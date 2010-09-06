from django.db import models
from django.db import transaction
from django.core import serializers
from django.utils.translation import ugettext_lazy as _

from datetime import date, datetime, timedelta
import tempfile
import zipfile


class Task(models.Model):
	title = models.CharField(max_length=100, help_text = _("The name of the Task"))
	description = models.TextField(help_text = _("Description of the assignment."))
	publication_date = models.DateTimeField(help_text = _("The date on which the user will see the task."))
	submission_date = models.DateTimeField(help_text = _("The date up until the user has time to complete the task."))
	model_solution = models.OneToOneField('solutions.Solution', blank=True, null=True, related_name='yetAnotherTaskLink')
	all_checker_finished = models.BooleanField(default=False, editable=False, help_text = _("Indicates whether the checker which don't run immediately on submission have been executed."))
	
	def __unicode__(self):
		return self.title
		
	def solutions(self,user):
		"""get solutions of the specified user"""
		return self.solution_set.filter(author=user)
		
	def checker(self):
		return self.AnonymityChecker_set.all() + self.LineCounter_set.all()
		
	def expired(self):
		"""docstring for expired"""
		return self.submission_date + timedelta(hours=1) < datetime.now()
		
	@classmethod
	def export_Tasks(cls, qureyset):
		""" Serializes a task queryset and related checkers to xml and bundels it with all files into a zipfile  """
		from praktomat.checker.models import Checker
		
		# fetch tasks, media objects, checker and serialize
		task_ids = qureyset.values_list('id', flat=True)
		task_objects = list(qureyset)
		media_objects = list( MediaFile.objects.filter(task__in=task_ids) )
		checker_classes = filter(lambda x:issubclass(x,Checker), models.get_models())
		checker_objects = sum(map(lambda x: list(x.objects.filter(task__in=task_ids)), checker_classes),[])
		data = serializers.serialize("xml", task_objects + media_objects + checker_objects)
		
		# fetch files
		files = []
		for checker_object in checker_objects:
			file_fields = filter(lambda x: isinstance(x, models.FileField) , checker_object.__class__._meta.fields)
			files += map(lambda file_field: checker_object.__getattribute__(file_field.attname), file_fields)
		for media_object in media_objects:
			files.append(media_object.media_file)
		
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
	def import_Tasks(cls, zip_file):
		zip = zipfile.ZipFile(zip_file,'r')
		data = zip.read('data.xml')
		id_map = {}
		for deserialized_object in serializers.deserialize("xml", data):
			object = deserialized_object.object
			if isinstance(object, Task):
				# save all tasks and their old id 
				old_id = object.id
				object.publication_date = date.max
				object.id = None
				deserialized_object.save()	
				id_map[old_id] = object.id
			else:
				# save media and checker, update task id
				object.id = None
				object.task_id = id_map[object.task_id]
				
				from django.core.files import File
				for file_field in filter(lambda x: isinstance(x, models.FileField) , object.__class__._meta.fields):
					file_field_instance = object.__getattribute__(file_field.attname)
					temp_file = tempfile.NamedTemporaryFile()						# autodeleted
					temp_file.write(zip.open(file_field_instance.name).read())
					file_field_instance.save(file_field_instance.name, File(temp_file))
				deserialized_object.save()
				
class MediaFile(models.Model):
	task = models.ForeignKey(Task)
	from django.conf import settings
	media_file = models.FileField(storage=settings.STORAGE, upload_to='TaskMediaFiles/')