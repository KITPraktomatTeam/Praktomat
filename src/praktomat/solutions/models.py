# -*- coding: utf-8 -*-

import zipfile
import tempfile
import mimetypes
import shutil

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.db.models import Max

import os, re

from praktomat.accounts.models import User
from praktomat.utilities import encoding, file_operations

class Solution(models.Model):
	""" """
	
	number = models.IntegerField(null=False, editable=False, help_text = _("Id unique in task and user.Eg. Solution 1 of user X in task Y in contrast to global solution Z"))
	
	task = models.ForeignKey('tasks.task')
	author = models.ForeignKey(User)
	creation_date = models.DateTimeField(auto_now_add=True)
	
	accepted = models.BooleanField( default = True, help_text = _('Indicates whether the solution has passed all public and required tests'))
	warnings = models.BooleanField( default = False, help_text = _('Indicates whether the solution has at least failed one public and not required tests'))
	plagiarism = models.BooleanField( default = False, help_text = _('Indicates whether the solution is a rip-off of another one.'))
	

	def __unicode__(self):
		return unicode(self.task) + ":" + unicode(self.author) + ":" + unicode(self.number)
	
	def final(self):
		""" return whether this is the last submission of this user """
		return self.id == Solution.objects.filter(task__id=self.task.id).filter(author=self.author.id).aggregate(Max('id'))['id__max']
	final.boolean = True

	def publicCheckerResults(self):
		# return self.checkerresult_set.filter(public=True) won't work, because public() isn't a field of result!
		return filter(lambda x: x.public(), self.checkerresult_set.all())
		
	def copySolutionFiles(self, toTempDir):
		for file in self.solutionfile_set.all():
			file.copyTo(toTempDir)
	
	def save(self, *args, **kwargs):
		"""Override save calculate the number on first save"""
		if self.number == None:
			self.number = (self.task.solution_set.filter(author=self.author).aggregate(Max('number'))['number__max'] or 0) + 1
		super(Solution, self).save(*args, **kwargs) # Call the "real" save() method.	
	
	def check(self, run_secret = 0): 
		"""Builds and tests this solution."""
		from praktomat.checker.models import check
		check(self, run_secret)

	def attestations_by(self, user):
		return self.attestation_set.filter(author=user)

	def copy(self):
		""" create a copy of this solution """
		solutionfiles = self.solutionfile_set.all()
		checkerresults = self.checkerresult_set.all()
		self.id = None
		self.number = None
		self.save()
		for file in solutionfiles:
			file.id = None
			file.solution = self
			file.save()
		for result in checkerresults:
			result.id = None
			result.solution = self
			result.save()




class SolutionFile(models.Model):
	"""docstring for SolutionFile"""
	
	def _get_upload_path(instance, filename):
		solution = instance.solution
		return 'SolutionArchive/Task_' + unicode(solution.task.id) + '/User_' + solution.author.username + '/Solution_' + unicode(solution.id) + '/' + filename
	
	solution = models.ForeignKey(Solution)
	file = models.FileField(upload_to = _get_upload_path,  help_text = _('Source code file as part of a solution or Zip file containing multiple solution files.')) 
	mime_type = models.CharField(max_length=100, help_text = _("Guessed file type. Automatically  set on save()."))
	
	# ignore hidden or os-specific files, etc. in zipfiles 
	regex = r'(' + '|'.join([	
						r'(^|/)\..*', 		# files starting with a dot (unix hidden files)
						r'__MACOSX/.*',
						r'^/.*',			# path starting at the root dir
						r'\.\..*',			# parent folder with '..'
						r'/$',				# don't unpack folders - the zipfile package will create them on demand
					]) + r')'
	
	ignorred_file_names_re = re.compile(regex)
	
	def save(self, force_insert=False, force_update=False, using=None):
		""" override save method to automatically expand zip files"""
		if self.file.name[-3:].upper() == 'ZIP':
			zip = zipfile.ZipFile(self.file, 'r')
			for zip_file_name in zip.namelist():
				if not self.ignorred_file_names_re.search(zip_file_name):
					new_solution_file = SolutionFile(solution=self.solution)
					temp_file = tempfile.NamedTemporaryFile()									# autodeleted
					temp_file.write(zip.open(zip_file_name).read()) 
					new_solution_file.file.save(zip_file_name, File(temp_file), save=True)		# need to check for filenames begining with / or ..?
		else:
			self.mime_type = mimetypes.guess_type(self.file.name)[0]
			models.Model.save(self, force_insert, force_update, using)
	
	def __unicode__(self):
		return self.file.name.rpartition('/')[2]
	
	def isBinary(self):
		return self.mime_type[:4] != "text"

	def isImage(self):
		return self.mime_type[:5] == "image"
	
	def path(self):
		""" path of file relative to the zip file, which once contained it """
		return self.file.name[len(self._get_upload_path('')):]
		
	def content(self):
		"""docstring for content"""
		if self.isBinary():
			return "Binary Data"
		else:
			return encoding.get_unicode(self.file.read())
					
	def copyTo(self,directory):
		""" Copies this file to the given directory """
		new_file_path = os.path.join(directory, self.path())
		if self.isBinary():
			shutil.copy(self.file.file.name, new_file_path)
		else:
			file_operations.create_file(new_file_path, self.content())
