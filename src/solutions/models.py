# -*- coding: utf-8 -*-

import zipfile
import tempfile
import mimetypes
import shutil
import os, re, string

from M2Crypto import RSA, EVP

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.db.models import Max
from django.conf import settings
from django.template.loader import render_to_string

from accounts.models import User
from utilities import encoding, file_operations
from configuration import get_settings

class Solution(models.Model):
	""" """
	
	number = models.IntegerField(null=False, editable=False, help_text = _("Id unique in task and user.Eg. Solution 1 of user X in task Y in contrast to global solution Z"))
	
	task = models.ForeignKey('tasks.task')
	author = models.ForeignKey(User, verbose_name="solution author")
	creation_date = models.DateTimeField(auto_now_add=True)
	
	accepted = models.BooleanField( default = False, help_text = _('Indicates whether the solution has passed all public and required tests'))
	warnings = models.BooleanField( default = False, help_text = _('Indicates whether the solution has at least failed one public and not required tests'))
	plagiarism = models.BooleanField( default = False, help_text = _('Indicates whether the solution is a rip-off of another one.'))
	final = models.BooleanField( default = False, help_text = _('Indicates whether this solution is the last (accepted) of the author.'))
	
	def __unicode__(self):
		return unicode(self.task) + ":" + unicode(self.author) + ":" + unicode(self.number)

	def allCheckerResults(self):
		return sorted(self.checkerresult_set.all(), key=lambda result: result.checker.order)

	def publicCheckerResults(self):
		# return self.checkerresult_set.filter(checker__public=True) won't work, because checker is a genericForeignKey!
		return sorted(filter(lambda x: x.public(), self.checkerresult_set.all()), key = lambda result: result.checker.order)
		
	def copySolutionFiles(self, toTempDir):
		for file in self.solutionfile_set.all():
			file.copyTo(toTempDir)
	
	def save(self, *args, **kwargs):
		"""Override save calculate the number on first save"""
		if self.number == None:
			self.number = (self.task.solution_set.filter(author=self.author).aggregate(Max('number'))['number__max'] or 0) + 1
		if self.final:
			# delete old final flag if this is the new final solution
			self.task.solutions(self.author).update(final=False)
		super(Solution, self).save(*args, **kwargs) # Call the "real" save() method.	
	
	def check(self, run_secret = 0): 
		"""Builds and tests this solution."""
		from checker.models import check
		check(self, run_secret)

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


def sign(file):
	if not settings.PRIVATE_KEY:
		return None
	evp = EVP.load_key(settings.PRIVATE_KEY)
	evp.sign_init()
	file.seek(0) 
	evp.sign_update(file.read())
	# signature to log for email, so shorten it
	s = EVP.MessageDigest('md5')
	s.update(evp.sign_final())
	return s.digest().encode('hex')

def verify(file, signature):
	return sign(file) == signature


class SolutionFile(models.Model):
	"""docstring for SolutionFile"""
	
	def _get_upload_path(instance, filename):
		solution = instance.solution
		return 'SolutionArchive/Task_' + unicode(solution.task.id) + '/User_' + solution.author.username + '/Solution_' + unicode(solution.id) + '/' + filename
	
	solution = models.ForeignKey(Solution)
	file = models.FileField(upload_to = _get_upload_path, max_length=500, help_text = _('Source code file as part of a solution or Zip file containing multiple solution files.')) 
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
					zip_file_name = zip_file_name  if isinstance(zip_file_name, unicode) else unicode(zip_file_name,errors='replace')
					new_solution_file.file.save(zip_file_name, File(temp_file), save=True)		# need to check for filenames begining with / or ..?
		else:
			self.mime_type = mimetypes.guess_type(self.file.name)[0]
			models.Model.save(self, force_insert, force_update, using)
	
	def __unicode__(self):
		return self.file.name.rpartition('/')[2]
	
	def get_hash(self):
		self.file.seek(0)
		s = EVP.MessageDigest('md5')
		s.update(self.file.read())
		return s.digest().encode('hex')
	
	def get_signature(self):
		return sign(self.file)			
	
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
			full_directory = os.path.join(directory,os.path.dirname(self.path()))
			if not os.path.exists(full_directory):
				file_operations.makedirs(full_directory)
			shutil.copy(self.file.file.name, new_file_path)
		else:
			file_operations.create_file(new_file_path, self.content())

def get_solutions_zip(solutions):
	
	zip_file = tempfile.SpooledTemporaryFile()
	zip = zipfile.ZipFile(zip_file,'w')
	for solution in solutions:
		# TODO: make this work for anonymous attesration, too
		if get_settings().anonymous_attestation:
			project_path = 'User' + index
			project_name = 'User ' + index 
		else:
			project_path = path_for_user(solution.author)
			project_name = solution.author.get_full_name() 
		base_name = path_for_task(solution.task) + '/' + project_path + '/'

		zip.writestr((base_name+'.project').encode('cp437'), render_to_string('solutions/eclipse/project.xml', { 'name': project_name }).encode("utf-8"))
		zip.writestr((base_name+'.classpath').encode('cp437'), render_to_string('solutions/eclipse/classpath.xml', { }))
		
		for index, solutionfile in enumerate(solution.solutionfile_set.all()):
			file = solutionfile.file
			name = (base_name + solutionfile.path()).encode('cp437','ignore')
			zip.write(file.path, name)
	zip.close()	
	zip_file.seek(0)
	return zip_file

def ascii_without(chars):
	return string.maketrans('','').translate(None,chars)

non_ascii_letters            = ascii_without(string.ascii_letters)
non_ascii_letters_and_digits = ascii_without(string.ascii_letters + string.digits)

def path_for_user(user):
	return user.get_full_name().encode('ascii','ignore').translate(None,non_ascii_letters)+'-'+str(user.mat_number)+'-'+str(user.id)

def path_for_task(task):
	return task.title.encode('ascii','ignore').translate(None,non_ascii_letters_and_digits)

path_regexp = re.compile(r'[^-]*-[^-]*-(.*)')

def id_for_path(path):
	return path_regexp.match(path).group(1)

