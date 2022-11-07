# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import zipfile
import tempfile
import mimetypes
import shutil
import os, re

from hashlib import sha256

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.db.models import Max
from django.db import transaction
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.core.mail import EmailMessage

from accounts.models import User
from utilities import encoding, file_operations
from configuration import get_settings

# TODO: This is duplicated from solutions/forms.py. Where should this go?
for (mimetype, extension) in settings.MIMETYPE_ADDITIONAL_EXTENSIONS:
    mimetypes.add_type(mimetype, extension, strict=True)

@python_2_unicode_compatible
class Solution(models.Model):
    """ """

    number = models.IntegerField(null=False, editable=False, help_text = _("Id unique in task and user. E.g. Solution 1 of user X in task Y in contrast to global solution Z"))

    task = models.ForeignKey('tasks.task', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="solution author")
    creation_date = models.DateTimeField(auto_now_add=True)

    testupload = models.BooleanField( default = False, help_text = _('Indicates whether this solution is a test upload.'))
    accepted = models.BooleanField( default = False, help_text = _('Indicates whether the solution has passed all public and required tests.'))
    warnings = models.BooleanField( default = False, help_text = _('Indicates whether the solution has at least failed one public and not required test.'))
    plagiarism = models.BooleanField( default = False, help_text = _('Indicates whether the solution is a rip-off of another one.'))
    final = models.BooleanField( default = False, help_text = _('Indicates whether this solution is the last (accepted) of the author.'))

    def __str__(self):
        return "%s:%s:%s" % (self.task, self.author , self.number)
        #return str(self.task) + ":" + str(self.author) + ":" + str(self.number)

    def allCheckerResults(self):
        results = self.checkerresult_set.all().prefetch_related('artefacts')
        return until_critical(sorted(results, key=lambda result: result.checker.order))

    def publicCheckerResults(self):
        # return self.checkerresult_set.filter(checker__public=True) won't work, because checker is a genericForeignKey!
        results = self.checkerresult_set.all().prefetch_related('artefacts')
        return until_critical(sorted([x for x in self.checkerresult_set.all() if x.public()], key = lambda result: result.checker.order))

    def copySolutionFiles(self, toTempDir):
        for file in self.solutionfile_set.all():
            file.copyTo(toTempDir)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Override save calculate the number on first save"""
        if self.number == None:
            self.number = (self.task.solution_set.filter(author=self.author).aggregate(Max('number'))['number__max'] or 0) + 1
        if self.final:
            # delete old final flag if this is the new final solution
            self.task.solutions(self.author).update(final=False)
            # may need to re-run jplag
            self.task.need_to_re_run_jplag()
        super(Solution, self).save(*args, **kwargs) # Call the "real" save() method.

    def check_solution(self, run_secret = 0, debug_keep_tmp = False):
        """Builds and tests this solution."""
        from checker.basemodels import check_solution
        check_solution(self, run_secret, debug_keep_tmp)

    def attestations_by(self, user):
        return self.attestation_set.filter(author=user)

    def copy(self):
        """ create a copy of this solution """
        self.final = False
        self.save()
        solutionfiles = self.solutionfile_set.all()
        checkerresults = self.checkerresult_set.all()
        self.id = None
        self.number = None
        self.final = True
        self.save()
        for file in solutionfiles:
            file.id = None
            file.solution = self
            file.save()
        for result in checkerresults:
            result.id = None
            result.solution = self
            result.save()

    def textSolutionFiles(self):
        return [file for file in self.solutionfile_set.all() if (not file.isBinary()) ]

    def displayableSolutionFiles(self):
        return [file for file in self.solutionfile_set.all() if (not file.isBinary() or file.isImage() or file.isEmbeddable())]


def until_critical(l):
    res = []
    for r in l:
        res.append(r)
        if r.is_critical():
            break
    return res

def get_solutionfile_upload_path(instance, filename):
    solution = instance.solution
    return 'SolutionArchive/Task_' + str(solution.task.id) + '/User_' + solution.author.username.replace("/","\u2044") + '/Solution_' + str(solution.id) + '/' + filename

@python_2_unicode_compatible
class SolutionFile(models.Model):
    """docstring for SolutionFile"""

    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    file = models.FileField(upload_to = get_solutionfile_upload_path, max_length=500, help_text = _('Source code file as part of a solution an archive file (.zip) containing multiple solution files.'))
    mime_type = models.CharField(max_length=100, help_text = _("Guessed file type. Automatically  set on save()."))

    # ignore hidden or os-specific files, etc. in zipfiles
    regex = r'(' + '|'.join([
                        r'(^|/)\..*',         # files starting with a dot (unix hidden files)
                        r'__MACOSX/.*',
                        r'^/.*',            # path starting at the root dir
                        r'\.\..*',            # parent folder with '..'
                        r'/$',                # don't unpack folders - the zipfile package will create them on demand
                    ]) + r')'

    ignorred_file_names_re = re.compile(regex)

    def save(self, force_insert=False, force_update=False, using=None):
        """ override save method to automatically expand zip files"""
        if self.file.name.upper().endswith('.ZIP'):
            zip = zipfile.ZipFile(self.file, 'r')
            for zip_file_name in zip.namelist():
                if not self.ignorred_file_names_re.search(zip_file_name):
                    new_solution_file = SolutionFile(solution=self.solution)
                    temp_file = tempfile.NamedTemporaryFile()                                    # autodeleted
                    temp_file.write(zip.open(zip_file_name).read())
                    import sys  # stay python 2 python 3 compatible
                    PY2 = sys.version_info[0] == 2
                    PY3 = sys.version_info[0] == 3
                    if PY3:
                        string_types = str
                    else:
                        string_types = unicode
                    zip_file_name = zip_file_name  if isinstance(zip_file_name, string_types) else string_types(zip_file_name, errors='replace')
                    new_solution_file.file.save(zip_file_name, File(temp_file), save=True)        # need to check for filenames begining with / or ..?
        else:
            self.mime_type = mimetypes.guess_type(self.file.name)[0]
            models.Model.save(self, force_insert, force_update, using)

    def __str__(self):
        return self.file.name.rpartition('/')[2]

    def get_hash(self):
        self.file.seek(0)
        s = sha256()
        s.update(self.file.read())
        return s.hexdigest()

    def isBinary(self):
        return self.mime_type[:4] != "text"

    def isImage(self):
        return self.mime_type[:5] == "image"

    def isEmbeddable(self):
        return self.mime_type in ("application/pdf",)

    def path(self):
        """ path of file relative to the zip file, which once contained it """
        # dont use length of filename as in original Code but use reg-expression!!
        # Original Code was:
        # return self.file.name[len(get_solutionfile_upload_path(self, '')):]

        # Fix for: https://github.com/KITPraktomatTeam/Praktomat/issues/232
        # It is realy saver not to use the length, i.e. if someone resubmit a solution via button and the new solution-number switched
        # from xxxx to yyyyy, the first letter of filename get lost if here only the length was used!!

        # TODO: Refactoring at the end of file there is a regexpr-based function "id_for_path(path)"
        #       should or could we used that function here?
        #
        # This fix for https://github.com/KITPraktomatTeam/Praktomat/issues/232
        # is used at H-BRS since May 2016 (Robert Hartmann)
        mytmpPattern = r'^SolutionArchive/Task_\d+/User_\S+/Solution_\d+/(.+)'
        return re.match(mytmpPattern, self.file.name).group(1) # for playing with reg see:  http://pythex.org/


    def content(self):
        """docstring for content"""
        if self.isBinary():
            return "Binary Data"
        else:
            return encoding.get_unicode(self.file.read())

    def copyTo(self, directory):
        """ Copies this file to the given directory """
        new_file_path = os.path.join(directory, self.path())
        if self.isBinary():
            full_directory = os.path.join(directory, os.path.dirname(self.path()))
            if not os.path.exists(full_directory):
                file_operations.makedirs(full_directory)
            shutil.copy(self.file.file.name, new_file_path)
        else:
            file_operations.create_file(new_file_path, self.content())

# from http://stackoverflow.com/questions/5372934
@receiver(post_delete, sender=SolutionFile)
def solution_file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    filename = os.path.join(settings.UPLOAD_ROOT, instance.file.name)
    instance.file.delete(False)
    # Remove left over empty directories
    dirname = os.path.dirname(filename)
    try:
        while os.path.basename(dirname) != "SolutionArchive":
            os.rmdir(dirname)
            dirname = os.path.dirname(dirname)
    except OSError:
        pass



class DummyFile:
    def __init__(self, path):
        self.path = path


def get_solutions_zip(solutions,include_copy_checker_files=False,include_artifacts=False):
    zip_file = tempfile.TemporaryFile()
    zip = zipfile.ZipFile(zip_file, 'w', allowZip64 = True)
    praktomat_files_destination          = "praktomat-files/"
    testsuite_destination                = praktomat_files_destination + "testsuite/"
    createfile_checker_files_destination = praktomat_files_destination + "other/"
    script_checker_files_destination     = praktomat_files_destination + "other/"
    checkstyle_checker_files_destination = praktomat_files_destination + "checkstyle/"
    artefact_files_destination           = praktomat_files_destination + "artefacts/"
    solution_files_destination           = "solution/"

    tmpdir = None
    createfile_checker_files_destinations = []
    createfile_checker_files = []

    if include_copy_checker_files:
        createfile_checker = { checker for solution in solutions for checker in solution.task.createfilechecker_set.all().filter(include_in_solution_download=True) }
        createfile_checker_files = [(createfile_checker_files_destination + checker.path + '/' + checker.path_relative_to_sandbox(),        checker.file)          for checker in createfile_checker if not checker.unpack_zipfile]
        # Temporary build directory
        sandbox = settings.SANDBOX_DIR
        tmpdir = file_operations.create_tempfolder(sandbox)
        for zipchecker in [ checker for checker in createfile_checker if checker.unpack_zipfile ]:
            cleanpath = zipchecker.path.lstrip("/ ")
            path = os.path.join(tmpdir, cleanpath)
            file_operations.unpack_zipfile_to(zipchecker.file.path, path,
                lambda n: None,
                lambda f: createfile_checker_files.append((
                    os.path.join(createfile_checker_files_destination, os.path.join(cleanpath, f)),
                    DummyFile(os.path.join(path, f))
                ))
            )
        createfile_checker_files_destinations = {createfile_checker_files_destination + checker.path for checker in createfile_checker if checker.is_sourcecode}



    for solution in solutions:
        # TODO: make this work for anonymous attestation, too
        if get_settings().anonymous_attestation:
            project_path = 'User' + index
            project_name = str(solution.task) + "-" + 'User ' + index
        else:
            project_path = path_for_user(solution.author)
            project_name = str(solution.task) + "-" + solution.author.get_full_name()
        base_name = path_for_task(solution.task) + '/' + project_path + '/'

        # We need to pass unicode strings to ZipInfo to ensure that it sets bit
        # 11 appropriately if the filename contains non-ascii characters.
        import sys  # stay python 2 python 3 compatible
        PY2 = sys.version_info[0] == 2
        PY3 = sys.version_info[0] == 3
        if PY3:
            string_types = str
        else:
            string_types = unicode

        assert isinstance(base_name, string_types)

        checkstyle_checker_files = []
        script_checker_files     = []
        artefact_files           = []
        junit3 = False
        junit4 = False
        checkstyle = False
        if include_copy_checker_files:
            checkstyle_checker = solution.task.checkstylechecker_set.all()
            script_checker     = solution.task.scriptchecker_set.all()
            junit_checker      = solution.task.junitchecker_set.all()
            junit3     = bool([ 0 for j in junit_checker if  j.junit_version == 'junit3' ])
            junit4     = bool([ 0 for j in junit_checker if  j.junit_version == 'junit4' ])
            checkstyle = bool(checkstyle_checker)

            checkstyle_checker_files = [(checkstyle_checker_files_destination + os.path.basename(checker.configuration.name), checker.configuration) for checker in checkstyle_checker]
            script_checker_files     = [(script_checker_files_destination     + checker.path_relative_to_sandbox(),    checker.shell_script)  for checker in script_checker]

        if include_artifacts:
            artefacts = [ artefact for result in solution.allCheckerResults() for artefact in result.artefacts.all() ]
            artefact_files = [(artefact_files_destination + os.path.basename(artefact.file.name), artefact.file) for artefact in artefacts]

        zip.writestr(base_name+'.project', render_to_string('solutions/eclipse/project.xml', { 'name': project_name, 'checkstyle' : checkstyle }).encode("utf-8"))
        zip.writestr(base_name+'.settings/org.eclipse.jdt.core.prefs', render_to_string('solutions/eclipse/settings/org.eclipse.jdt.core.prefs', { }).encode("utf-8"))

        zip.writestr(base_name+'.classpath', render_to_string('solutions/eclipse/classpath.xml', {'junit3' : junit3, 'junit4': junit4, 'createfile_checker_files' : include_copy_checker_files, 'createfile_checker_files_destinations' : createfile_checker_files_destinations, 'testsuite_destination' : testsuite_destination }).encode("utf-8"))
        if checkstyle:
            zip.writestr(base_name+'.checkstyle', render_to_string('solutions/eclipse/checkstyle.xml', {'checkstyle_files' : [filename for (filename, _) in checkstyle_checker_files], 'createfile_checker_files_destination' : createfile_checker_files_destination, 'testsuite_destination' : testsuite_destination }).encode("utf-8"))

        if junit4:
            zip.writestr(base_name+testsuite_destination+'AllJUnitTests.java', render_to_string('solutions/eclipse/AllJUnitTests.java', { 'testclasses' : [ j.class_name for j in junit_checker if j.junit_version == 'junit4' ]}).encode("utf-8"))
            zip.writestr(base_name+praktomat_files_destination+'AllJUnitTests.launch', render_to_string('solutions/eclipse/AllJUnitTests.launch', { 'project_name' : project_name, 'praktomat_files_destination' : praktomat_files_destination}).encode("utf-8"))
            zip.write(os.path.dirname(__file__)+"/../checker/scripts/eclipse-junit.policy", (base_name+praktomat_files_destination+'eclipse-junit.policy'))

        solution_files  = [ (solution_files_destination+solutionfile.path(), solutionfile.file) for solutionfile in solution.solutionfile_set.all()]

        for (name, file) in solution_files + createfile_checker_files + checkstyle_checker_files + script_checker_files + artefact_files:
            zippath = os.path.normpath(base_name + name)

            import sys  # stay python 2 python 3 compatible
            PY2 = sys.version_info[0] == 2
            PY3 = sys.version_info[0] == 3
            if PY3:
                string_types = str
            else:
                string_types = unicode

            assert isinstance(zippath, string_types)
            try: # Do not overwrite files from the solution by checker files
                zip.getinfo(zippath)
            except KeyError:
                zip.write(file.path, zippath)
                assert zip.getinfo(zippath) # file was really added under name "zippath" (not only some normalization thereof)

    zip.close()
    zip_file.seek(0)

    if include_copy_checker_files:
        if (tmpdir is None) or (not os.path.isdir(tmpdir)) or (not os.path.basename(tmpdir).startswith("tmp")):
            raise Exception("Invalid tmpdir: " + tmpdir)
        shutil.rmtree(tmpdir)

    return zip_file

def path_for_user(user):
    return user.get_full_name().replace("/","\u2044")+'-'+str(user.mat_number)+'-'+str(user.id)

def path_for_task(task):
    return task.title

path_regexp = re.compile(r'[^-]*-[^-]*-(.*)')

def id_for_path(path):
    return path_regexp.match(path).group(1)

class ConfirmationMessage(EmailMessage):
    """
    Special EmailMessage to combine headers set by OpenSSL S/MIME and django sendmail.
    """
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, cc=None,
                 reply_to=None):
        super(ConfirmationMessage, self).__init__(
            subject, body, from_email, to, bcc, connection, attachments,
            headers, cc, reply_to,
        )

    def message(self):
        message = super(ConfirmationMessage, self).message()
        return MessageWrapper(message)

class MessageWrapper():
    def __init__(self, message):
        self.message = message

    # Django supplies Strings as "linesep" (and not Bytes)
    def as_bytes(self, linesep='\n'):
        # byte version of linesep
        linesep_bytes = linesep.encode('ascii')
        # Construct the message with the full S/MIME mail as body
        msg = self.message.as_bytes(linesep=linesep)
        # Now, use the S/MIME headers as headers for the email
        lines = msg.split(linesep_bytes)
        if (lines[0] != b'Content-Type: text/plain; charset="utf-8"' or
                lines[1] != b'MIME-Version: 1.0' or
                not re.match(b'Content-Transfer-Encoding: (7|8)bit', lines[2])):
            raise AssertionError('Assumptions on message format violated')
        i = lines.index(b'')
        j = lines[i+1:].index(b'') + i + 1
        transformed = lines[i+1:j] + lines[3:i] + lines[j+1:]
        return linesep_bytes.join(transformed)

    def get_charset(self):
        return None
