from datetime import date, datetime, timedelta
import tempfile
import zipfile

from django.db import models
from django.db import transaction
from django import db
from django.core import serializers
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Max

from utilities.deleting_file_field import DeletingFileField


class Task(models.Model):
	title = models.CharField(max_length=100, help_text = _("The name of the Task"))
	description = models.TextField(help_text = _("Description of the assignment."))
	publication_date = models.DateTimeField(help_text = _("The time on which the user will see the task."))
	submission_date = models.DateTimeField(help_text = _("The time up until the user has time to complete the task. This time will be extended by one hour for those who yust missed the deadline."))
	supported_file_types = models.CharField(max_length=1000, default ="^(text/.*|image/.*)$", help_text = _("Regular Expression describing the mime types of solution files that the user is allowed to upload."))
	max_file_size = models.IntegerField(default=1000, help_text = _("The maximum size of an uploaded solution file in kilobyte."))
	model_solution = models.ForeignKey('solutions.Solution', blank=True,
			null=True, related_name='model_solution_task')
	all_checker_finished = models.BooleanField(default=False, editable=False, help_text = _("Indicates whether the checker which don't run immediately on submission have been executed."))
	final_grade_rating_scale = models.ForeignKey('attestation.RatingScale', null=True, help_text = _("The scale used to mark the hole solution."))
	
	def __unicode__(self):
		return self.title
		
	def solutions(self,user):
		""" get ALL solutions of the specified user """
		return self.solution_set.filter(author=user)
	
	def final_solution(self,user):
		""" get FINAL solution of specified user """
		solutions = self.solution_set.filter(author=user, final=True)
		return solutions[0] if solutions else None
		
	def expired(self):
		"""docstring for expired"""
		return self.submission_date + timedelta(hours=1) < datetime.now()
	
	def check_all_final_solutions(self):
		from checker.models import check_multiple
		check_multiple(self.solution_set.filter(final=True), True)

		if self.expired():
				self.all_checker_finished = True
				self.save()

	@classmethod
	def export_Tasks(cls, qureyset):
		""" Serializes a task queryset and related checkers to xml and bundels it with all files into a zipfile  """
		from checker.models import Checker
		from solutions.models import Solution, SolutionFile

		# fetch tasks, media objects, checker and serialize
		task_objects = list(qureyset)
		media_objects = list( MediaFile.objects.filter(task__in=task_objects) )
		model_solution_objects = list( Solution.objects.filter(model_solution_task__in=task_objects) )
		model_solution_file_objects = list( SolutionFile.objects.filter(solution__in=model_solution_objects) )
		checker_classes = filter(lambda x:issubclass(x,Checker), models.get_models())
		checker_objects = sum(map(lambda x: list(x.objects.filter(task__in=task_objects)), checker_classes),[])
		data = serializers.serialize("xml", task_objects + media_objects + checker_objects + model_solution_objects + model_solution_file_objects)
		
		# fetch files
		files = []
		for checker_object in checker_objects:
			file_fields = filter(lambda x: isinstance(x, models.FileField) , checker_object.__class__._meta.fields)
			files += map(lambda file_field: checker_object.__getattribute__(file_field.attname), file_fields)
		for media_object in media_objects:
			files.append(media_object.media_file)
		for model_solution_file_object in model_solution_file_objects:
			files.append(model_solution_file_object.file)
		
		# zip it up
		zip_file = tempfile.SpooledTemporaryFile()
		zip = zipfile.ZipFile(zip_file,'w')
		zip.writestr('data.xml', data)
		for file in files:
			zip.write(file.path, file.name)
		zip.close()	
		zip_file.seek(0)		# rewind
		return zip_file			# return unclosed file-like object!?
		
	@classmethod
	@transaction.commit_on_success		# May not work with MySQL: see django docu
	def import_Tasks(cls, zip_file, solution_author):
		from solutions.models import Solution, SolutionFile
		zip = zipfile.ZipFile(zip_file,'r')
		data = zip.read('data.xml')
		task_id_map = {}
		solution_id_map = {}
		old_solution_to_new_task_map = {}
		solution_list = []
		for deserialized_object in serializers.deserialize("xml", data):
			object = deserialized_object.object
			old_id = object.id
			object.id = None
			if isinstance(object, Task):
				# save all tasks and their old id 
				object.publication_date = date.max
				deserialized_object.save()	
				task_id_map[old_id] = object.id
				old_solution_to_new_task_map[object.model_solution_id] = object.id
				object.model_solution = None
				object.final_grade_rating_scale = None
				deserialized_object.save()
			else:
				# save modelsolution, media and checker, update task id
				if isinstance(object, SolutionFile):
					object.solution_id = solution_id_map[object.solution_id]
				else:
					object.task_id = task_id_map[object.task_id]
				
				from django.core.files import File
				for file_field in filter(lambda x: isinstance(x, models.FileField) , object.__class__._meta.fields):
					file_field_instance = object.__getattribute__(file_field.attname)
					temp_file = tempfile.NamedTemporaryFile()						# autodeleted
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
			solution.check(run_secret=True)

								
class MediaFile(models.Model):

	def get_storage_path(instance, filename):
		return 'TaskMediaFiles/Task_%s/%s' % (instance.task.pk, filename)

	task = models.ForeignKey(Task)
	media_file = DeletingFileField(upload_to=get_storage_path, max_length=500)
