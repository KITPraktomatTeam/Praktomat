# -*- coding: utf-8 -*-

import zipfile
import tempfile

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.db.models import Max

import os, re, tempfile, shutil
 
from praktomat.accounts.models import User
from praktomat.utilities import encoding

class Solution(models.Model):
	"""docstring for Solution"""
	
	number = models.IntegerField(null=False, editable=False, help_text = _("Id unique in task and user.Eg. Solution 1 of user X in task Y in contrast to global solution Z"))
	
	task = models.ForeignKey('tasks.task')
	author = models.ForeignKey(User)
	creation_date = models.DateTimeField(auto_now_add=True)
	
	accepted = models.BooleanField( default = True, help_text = _('Indicates whether the solution has passed all public and required tests'))
	warnings = models.BooleanField( default = False, help_text = _('Indicates whether the solution has at least failed one public and not required tests'))
	
	final = models.BooleanField( default = False, help_text = _('Indicates whether the solution the solution is accepted and marked final by the author'))
	
	def __unicode__(self):
		return unicode(self.creation_date)
	
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
		
		# Delete previous results if the checker have allready been run
		self.checkerresult_set.all().delete()
		# set up environment
		from praktomat.checker.models import CheckerEnvironment, TMP_DIR_MODE
		env = CheckerEnvironment()
		sources = []
		for file in self.solutionfile_set.all(): 
			sources.append((unicode(file),file.content()))
		env.set_sources(sources)
		env.set_user(self.author)
		
		try:
			# Setting default temp dir location and creating it
			tempfile.tempdir = os.path.join(settings.UPLOAD_ROOT, "SolutionSandbox")
			new_tmpdir = tempfile.mktemp()

			# to access working directory by scripts
			os.system("export PRAKTOMAT_WORKING_DIR=" + `new_tmpdir`)
			env.set_tmpdir(new_tmpdir)
			
			os.makedirs(env.tmpdir(), TMP_DIR_MODE)
			os.chmod(env.tmpdir(), TMP_DIR_MODE)
			self.copySolutionFiles(env.tmpdir())
			self.run_checks(env, run_secret)
		finally:
			# reset default temp dir location 
			tempfile.tempdir = None
			# Delete temporary directory
			if not settings.DEBUG:
				try:
					shutil.rmtree(new_tmpdir)
				except IOError:
					pass
		
		
	
	def run_checks(self, env, run_all): # , task
		""" Check program. The case `Nothing submitted' is handled by the Saver.  Also,
		this does not work when submitting archives, since at this
		point, archives are not unpacked yet, and hence,
		env.main_module() returns the archive name => commented out. -AZ
		program = env.main_module()
		if not program: return """

		passed_checkers = []
		
		# Apply all checkers from TASK
		task = self.task
		# querysets can't be concatenated with +
		checkersets =[	task.anonymitychecker_set.all(),
						task.linecounter_set.all(),
						task.createfilechecker_set.all(),
						task.diffchecker_set.all(),
						task.scriptchecker_set.all(),
						task.interfacechecker_set.all(),
						task.linewidthchecker_set.all(),
						task.textchecker_set.all(),
						task.cxxbuilder_set.all(),
						task.cbuilder_set.all(),
						task.javabuilder_set.all(),
						task.javagccbuilder_set.all(),
						task.fortranbuilder_set.all(),
						task.dejagnusetup_set.all(), 
						task.dejagnutester_set.all(),
						task.checkstylechecker_set.all(), ]
		
		for checkers in checkersets:
			for checker in checkers:
				
				if (checker.always or run_all):
				
					# Check dependencies -> This requires the right order of the checkers
					can_run_checker = True
					for required_checker in checker.requires():
						have_required_checker = False
						for passed_checker in passed_checkers:
							if isinstance(passed_checker, required_checker):
								have_required_checker = True
						if not have_required_checker:
							can_run_checker = False
					
					if can_run_checker: 
						# Invoke Checker 
						result = checker.run(env)
					else:
						# make non passed result
						# this as well as the dependency check should propably go into checker class
						result = checker.result()
						result.set_log(u"Checker konnte nicht ausgeführt werden, da benötigte Checker nicht bestanden wurden.")
						result.set_passed(False)
						
					result.solution = self
					result.save()

					if not result.passed and checker.public:
						if checker.required:
							self.accepted = False
						else:
							self.warnings= True
							
					if result.passed:
						passed_checkers.append(checker)
		self.save()
		
	def attestations_by(self, user):
		return self.attestation_set.filter(author=user)
	

class SolutionFile(models.Model):
	"""docstring for SolutionFile"""
	
	def _get_upload_path(instance, filename):
		solution = instance.solution
		return 'SolutionArchive/Task_' + unicode(solution.task.id) + '/User_' + solution.author.username + '/Solution_' + unicode(solution.id) + '/' + filename
	
	solution = models.ForeignKey(Solution)
	file = models.FileField(storage=settings.STORAGE, upload_to = _get_upload_path,  help_text = _('Source code file as part of a solution or Zip file containing multiple solution files.')) 
	# File mime content types allowed to upload
	supported_types_re = re.compile(r'^(text/.*|application/octet-stream)$')
	# Ignore hidden and OS-specific files in zipfiles
	# .filename or __MACOSX/bla.txt or /rootdir or ..dirup
	ignorred_file_names_re = re.compile('^(\..*|__MACOSX/.*|/.*|\.\..*)$')
	
	def save(self, force_insert=False, force_update=False, using=None):
		""" override save method to automatically expand zip files"""
		if self.file.name[-3:].upper() == 'ZIP':
			zip = zipfile.ZipFile(self.file, 'r')
			for zip_file_name in zip.namelist():
				if not self.ignorred_file_names_re.match(zip_file_name):
					new_solution_file = SolutionFile(solution=self.solution)
					temp_file = tempfile.NamedTemporaryFile()									# autodeleted
					temp_file.write(zip.open(zip_file_name).read()) 
					new_solution_file.file.save(zip_file_name, File(temp_file), save=True)		# need to check for filenames begining with / or ..?
		else:
			models.Model.save(self, force_insert, force_update, using)
	
	def __unicode__(self):
		return self.file.name.rpartition('/')[2]
		
	def content(self):
		"""docstring for content"""
		return encoding.get_unicode(self.file.read()) 
		
	def copyTo(self,directory):
		""" Copies this file to the given directory """
		shutil.copy(self.file.path, directory)
		

