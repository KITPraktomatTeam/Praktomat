# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from datetime import date, datetime, timedelta
import tempfile
import zipfile
import os
import os.path
import shutil

from django.apps import apps
from django.db import models
from django.db import transaction
from django import db
from django.core import serializers
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Max

from configuration import get_settings

from utilities.deleting_file_field import DeletingFileField
from utilities.safeexec import execute_arglist

@python_2_unicode_compatible
class Task(models.Model):
    title = models.CharField(max_length=100, help_text = _("The name of the task"))
    description = models.TextField(help_text = _("Description of the assignment."))
    publication_date = models.DateTimeField(help_text = _("The time on which the user will see the task."))
    submission_date = models.DateTimeField(help_text = _("The time up until the user has time to complete the task. This time will be extended by the duration configured with the deadline tolerance setting for those who just missed the deadline."))

    submission_free_uploads = models.IntegerField(default=1, help_text =_("Number of submissions a user can make before waitdelta got active"))
    submission_waitdelta = models.IntegerField(default=0,help_text=_("Timedelta in minutes. The user must wait before submitting the next solution of same task: I removed the linear function: Timedelta multiplied with number of current uploads"))
    submission_maxpossible = models.IntegerField(default=-1,help_text=_("Number of uploads a user can submit for the same task. Value -1 means unlimited"))

    supported_file_types = models.CharField(max_length=1000, default ="^(text/.*|image/.*|application/pdf)$", help_text = _("Regular Expression describing the mime types of solution files that the user is allowed to upload."))
    max_file_size = models.IntegerField(default=1000, help_text = _("The maximum size of an uploaded solution file in kilobyte."))
    model_solution = models.ForeignKey('solutions.Solution', on_delete=models.SET_NULL, blank=True, null=True, related_name='model_solution_task')
    all_checker_finished = models.BooleanField(default=False, editable=False, help_text = _("Indicates whether the checker which don't run immediately on submission have been executed."))
    final_grade_rating_scale = models.ForeignKey('attestation.RatingScale', on_delete=models.SET_NULL, null=True, help_text = _("The scale used to mark the whole solution."))
    warning_threshold = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text = _("If the student has less points in his tasks than the sum of their warning thresholds, display a warning."))
    only_trainers_publish = models.BooleanField(default=False, help_text = _("Indicates that only trainers may publish attestations. Otherwise, tutors may publish final attestations within their tutorials."))
    jplag_up_to_date = models.BooleanField(default=False, help_text = _("No new solution uploads since the last jPlag run"))

    class Meta:
        ordering = ['submission_date', 'title']

    def __str__(self):
        return self.title

    def solutions(self, user):
        """ get ALL solutions of the specified user """
        return self.solution_set.filter(author=user)

    def final_solution(self, user):
        """ get FINAL solution of specified user """
        solutions = self.solution_set.filter(author=user, final=True)
        return solutions.first()

    def expired(self):
        """returns whether the task has expired"""
        return self.submission_date + get_settings().deadline_tolerance < datetime.now()

    def check_all_final_solutions(self):
        from checker.basemodels import check_multiple
        final_solutions = self.solution_set.filter(final=True)
        count = check_multiple(final_solutions, True)

        if self.expired():
            self.all_checker_finished = True
            self.save()
        return final_solutions.count()

    def check_all_latest_only_failed_solutions(self):
        from checker.basemodels import check_solution
        from accounts.models import User
        solution_queryset = self.solution_set
        final_solutions_queryset = solution_queryset.filter(final=True)
        final_users = set(final_solutions_queryset.values_list('author', flat=True))

        # All solutions from users without a final solution
        only_failed_solution_set = solution_queryset.exclude(author__in=final_users)
        # Users without a final solution (maybe without an upload at all)
        non_final_users = set(User.objects.all().values_list('id', flat=True)) - final_users

        count = 0
        for user in non_final_users:
            users_only_failed_solutions = only_failed_solution_set.filter(author=user)
            if users_only_failed_solutions.count() > 0:
                latest_only_failed_solution = users_only_failed_solutions.latest('number')
                check_solution(latest_only_failed_solution, True)
                count += 1
        return count

    def get_checkers(self):
        from checker.basemodels import Checker
        checker_app = apps.get_app_config('checker')

        checker_classes = [x for x in checker_app.get_models() if issubclass(x, Checker)]
        unsorted_checker = sum([list(x.objects.filter(task=self)) for x in checker_classes], [])
        checkers = sorted(unsorted_checker, key=lambda checker: checker.order)
        return checkers

    def jplag_dir_path(self):
        return os.path.join(settings.UPLOAD_ROOT, 'jplag', 'Task_' + str(self.id))

    def jplag_index_url(self):
        return os.path.join('jplag', 'Task_' + str(self.id), "index.html")

    def jplag_log_url(self):
        return os.path.join('jplag', 'Task_' + str(self.id), "jplag.txt")

    def did_jplag_run(self):
        return os.path.isdir(self.jplag_dir_path())

    def did_jplag_succeed(self):
        return os.path.exists(os.path.join(self.jplag_dir_path(), 'index.html'))

    def need_to_re_run_jplag(self):
        if self.jplag_up_to_date:
            self.jplag_up_to_date = False
            self.save()

    @staticmethod
    def jplag_languages():
        return { 'Java':     { 'param': 'java19', 'files': '.java,.JAVA' },
                 'R':        { 'param': 'text',   'files': '.R' },
                 'Python':   { 'param': 'text',   'files': '.py' },
                 'Isabelle': { 'param': 'text',   'files': '.thy' },
               }

    def run_jplag(self, lang):
        # sanity check
        if not hasattr(settings, 'JPLAGJAR'):
            raise RuntimeError("Setting JPLAGJAR not set")
        if not os.path.exists(settings.JPLAGJAR):
            raise RuntimeError("Setting JPLAGJAR points to non-existing file %s" % settings.JPLAGJAR)
        if not lang in self.jplag_languages():
            raise RuntimeError("Unknown jplag settings %s" % lang)

        # Remember jplag setting
        configuration = get_settings()
        configuration.jplag_setting = lang
        configuration.save()

        jplag_settings = self.jplag_languages()[lang]
        path = self.jplag_dir_path()
        tmp = os.path.join(path, "tmp")
        # clean out previous run
        if self.did_jplag_run():
            shutil.rmtree(path)
        # create output directory
        os.makedirs(path)

        # extract all final solutions
        os.mkdir(tmp)
        final_solutions = self.solution_set.filter(final=True)
        from solutions.models import path_for_user
        for solution in final_solutions:
            subpath = os.path.join(tmp, path_for_user(solution.author))
            os.mkdir(subpath)
            solution.copySolutionFiles(subpath)

        # run jplag
        args = [settings.JVM,
                "-jar", settings.JPLAGJAR,
                "-s",
                "-l", jplag_settings['param'],
                "-p", jplag_settings['files'],
                "-r", path,
                tmp]
        environ={}
        environ['LANG'] = settings.LANG
        environ['LANGUAGE'] = settings.LANGUAGE
        [output, error, exitcode, timed_out, oom_ed] = \
         execute_arglist(args, path, environment_variables=environ, unsafe=True)

        # remove solution copies
        shutil.rmtree(tmp)

        # write log file
        with open(os.path.join(path, "jplag.txt"), 'w') as fd:
            fd.write(output)

        # mark jplag as up-to-date
        self.jplag_up_to_date = True
        self.save()


    @classmethod
    def export_Tasks(cls, queryset):
        """ Serializes a task queryset and related checkers to xml and bundles it with all files into a zipfile  """
        from solutions.models import Solution, SolutionFile
        from attestation.models import RatingScaleItem

        # fetch tasks, media objects, checker and serialize
        task_objects = list(queryset)
        # prevent duplication of exported RatingScale objects
        rating_scale_objects = list( {t.final_grade_rating_scale for t in task_objects if t.final_grade_rating_scale} )
        rating_scale_item_objects = list( RatingScaleItem.objects.filter(scale__in=rating_scale_objects) )
        media_objects = list( MediaFile.objects.filter(task__in=task_objects) )
        model_solution_objects = list( Solution.objects.filter(model_solution_task__in=task_objects) )
        model_solution_file_objects = list( SolutionFile.objects.filter(solution__in=model_solution_objects) )

        from checker.basemodels import Checker
        checker_app = apps.get_app_config('checker')
        checker_classes = [x for x in checker_app.get_models() if issubclass(x, Checker)]
        checker_objects = sum([list(x.objects.filter(task__in=task_objects)) for x in checker_classes], [])
        # serialize RatingScale objects first since they are used by tasks
        data = serializers.serialize("xml", rating_scale_objects + rating_scale_item_objects + task_objects + media_objects + checker_objects + model_solution_objects + model_solution_file_objects)

        # fetch files
        files = []
        for checker_object in checker_objects:
            file_fields = [x for x in checker_object.__class__._meta.fields if isinstance(x, models.FileField)]
            files += [checker_object.__getattribute__(file_field.attname) for file_field in file_fields]
        for media_object in media_objects:
            files.append(media_object.media_file)
        for model_solution_file_object in model_solution_file_objects:
            files.append(model_solution_file_object.file)

        # zip it up
        zip_file = tempfile.SpooledTemporaryFile()
        zip = zipfile.ZipFile(zip_file, 'w')
        zip.writestr('data.xml', data)
        for file in files:
            zip.write(file.path, file.name)
        zip.close()
        zip_file.seek(0)        # rewind
        return zip_file            # return unclosed file-like object!?

    @classmethod
    @transaction.atomic
    def import_Tasks(cls, zip_file, solution_author, is_template=True):
        from solutions.models import Solution, SolutionFile
        from attestation.models import RatingScale, RatingScaleItem

        zip = zipfile.ZipFile(zip_file, 'r')

        import sys
        PY2 = sys.version_info[0] == 2
        PY3 = sys.version_info[0] == 3
        data = ""
        if PY3:
            data = zip.read('data.xml').decode('utf-8') #py3
        else:
            data = zip.read('data.xml') #Py2

        task_id_map = {}
        scale_map = {}
        solution_id_map = {}
        old_solution_to_new_task_map = {}
        solution_list = []
        for deserialized_object in serializers.deserialize("xml", data):
            object = deserialized_object.object
            old_id = object.id
            #since Django Debug Toolbar didn't catch logger output, I print to console while in debugging mode
            #import logging
            #logger = logging.getLogger(__name__)
            #logger.error("Test!")
            #print("======================================")
            #print('OldID: %s -- Type: %s '%(str(old_id) , str(type(object))))
            #print("======================================")

            # from Django docs: "if the pk attribute in the serialized data doesn’t exist or is null, a new instance will be saved to the database."
            # we want to save a task always as new database entry, therefor we set the object.id to None.
            # but we do not want to save RatingScale or RatingScaleItem, if equivalent elements are in database already.
            object.id = None
            if isinstance(object, Task):
            # save all tasks and their old id
                if is_template:
                    object.publication_date = date.max
                deserialized_object.save()
                task_id_map[old_id] = object.id
                #print("======================================")
                #print('OldID: %s -- NewID: %s -- Name: %s '%(str(old_id) , str(task_id_map[old_id]) , str(object.title)))
                #print("======================================")
                old_solution_to_new_task_map[object.model_solution_id] = object.id
                object.model_solution = None
                object.final_grade_rating_scale = None if is_template else scale_map.get(object.final_grade_rating_scale_id)
                deserialized_object.save()

            elif isinstance(object, RatingScale):
                if not is_template:
                    dbobject=RatingScale.objects.filter(name=object.name).order_by('id').first()
                    #if there is no RatingScale with the name in database, we save the deserialized_object, else we are reusing existent data.
                    if dbobject is None:
                        deserialized_object.save()
                        scale_map[old_id] = object
                        #print("======================================")
                        #print('>> OldID: %s -- NewID: %s -- Name: %s '%(str(old_id) , str(scale_map[old_id].id) , str(object)))
                        #print("======================================")
                    else:
                        scale_map[old_id] = dbobject
                        #print("======================================")
                        #print('>> OldID: %s -- ReusingID: %s -- Name: %s '%(str(old_id) , str(scale_map[old_id].id) , str(object)))
                        #print("======================================")
                    #print (scale_map)
                    #print("===============")

            elif isinstance(object, RatingScaleItem):
                if not is_template:
                    #if there is no RatingScaleItem with the same name for corresponding RatingScale in database,
                    #we save the deserialized_object, else we are reusing existent data.
                    #The consequence is: If you where importing tasks from different praktomat instances having differences in names of RatingScaleItems
                    #but using same name for RatingScale, than these ScaleItems become merge into the same RatingScale.
                    dbobject=RatingScaleItem.objects.filter(name=object.name, scale=scale_map[object.scale_id].id ).order_by('id').first()
                    if dbobject is None:
                        object.scale = scale_map[object.scale_id]
                        deserialized_object.save()
                        #print("======================================")
                        #print('>> OldID: %s -- NewID: %s -- Name: %s '%(str(old_id) , str(object.id) , str(object)))
                        #print("======================================")
                    #else:
                        #print("======================================")
                        #print('>> OldID: %s -- ReusingID: %s -- Name: %s '%(str(old_id) , str(dbobject.id) , str(dbobject)))
                        #print("======================================")

            else:
                # save modelsolution, media and checker, update task id
                if isinstance(object, SolutionFile):
                    object.solution_id = solution_id_map[object.solution_id]
                else:
                    object.task_id = task_id_map[object.task_id]

                from django.core.files import File
                for file_field in [x for x in object.__class__._meta.fields if isinstance(x, models.FileField)]:
                    file_field_instance = object.__getattribute__(file_field.attname)
                    temp_file = tempfile.NamedTemporaryFile()                        # autodeleted
                    temp_file.write(zip.open(file_field_instance.name).read())
                    file_field_instance.save(file_field_instance.name, File(temp_file))

                deserialized_object.save()

                if isinstance(object, Solution):
                    task = Task.objects.get(id=old_solution_to_new_task_map[old_id])
                    task.model_solution = object
                    task.save()
                    solution_id_map[old_id] = object.id
                    solution_list.append(object)
                    object.author = solution_author
                    object.save()

        for solution in solution_list:
            solution.check_solution(run_secret=True)

def get_mediafile_storage_path(instance, filename):
    return 'TaskMediaFiles/Task_%s/%s' % (instance.task.pk, filename)

def get_htmlinjectorfile_storage_path(instance, filename):
    return 'TaskHtmlInjectorFiles/Task_%s/%s' % (instance.task.pk, filename)


class MediaFile(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    media_file = DeletingFileField(upload_to=get_mediafile_storage_path, max_length=500)


class HtmlInjector(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    inject_in_solution_view      = models.BooleanField(
        default=False,
        help_text = _("Indicates whether HTML code shall be injected in public  solution views, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/solutions/5710/")
    )
    inject_in_solution_full_view = models.BooleanField(
        default=False,
        help_text = _("Indicates whether HTML code shall be injected in private solution views, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/solutions/5710/full")
    )
    inject_in_attestation_edit = models.BooleanField(
        default=True,
        help_text = _("Indicates whether HTML code shall be injected in attestation edits, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/attestation/134/edit")
    )
    inject_in_attestation_view = models.BooleanField(
        default=False,
        help_text = _("Indicates whether HTML code shall be injected in attestation views, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/attestation/134")
    )
    html_file = DeletingFileField(upload_to=get_htmlinjectorfile_storage_path, max_length=500)
