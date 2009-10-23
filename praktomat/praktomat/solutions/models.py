# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from praktomat.tasks.models import Task
from django.utils.translation import ugettext_lazy as _

import tempfile
import os
import shutil

class Solution(models.Model):
	"""docstring for Solution"""
	
	task = models.ForeignKey(Task)
	author = models.ForeignKey(User)
	creation_date = models.DateTimeField(auto_now_add=True)
	
	accepted = models.BooleanField( default = True, help_text = _('Indicates whether the solution has passed all public and required tests'))
	warnings = models.BooleanField( default = False, help_text = _('Indicates whether the solution has at least failed one public and not required tests'))
	
	def __unicode__(self):
		return unicode(self.creation_date)
	
	def publicCheckerResults(self):
		# return self.checkerresult_set.filter(public=True) won't work, because public() isn't a field of result!
		return filter(lambda x: x.public(), self.checkerresult_set.all())
		
	def copySolutionFiles(self, toTempDir):
		for file in self.solutionfile_set.all():
			file.copyTo(toTempDir)
	
	def check(self, verbose = 1, run_secret = 0): #task, user, key, course_id,
		"""Builds and tests this solution."""

		# set up environment
		from praktomat.checker.models import CheckerEnvironment, TMP_DIR_MODE
		env = CheckerEnvironment()
		sources = []
		for file in self.solutionfile_set.all(): 
			sources.append((unicode(file),file.content()))
		env.set_sources(sources)
		#if self.tab_width() > 0:				# unsure about that
		#	env.set_tab_width(self.tab_width())
		env.set_user(self.author)
		# env.set_key(key)						# what is the key?
		# env.set_course_id(course_id)			
		# env.set_task_id(self.task_id())		# set task insted of id
		
		# Setting default temp dir location and creating it
		tempfile.tempdir = settings.TMP_DIR
		new_tmpdir = tempfile.mktemp()

		# to access working directory by scripts
		os.system("export PRAKTOMAT_WORKING_DIR=" + `new_tmpdir`)
		#misc.log(`new_tmpdir`)
		env.set_tmpdir(new_tmpdir)
		os.mkdir(env.tmpdir(), TMP_DIR_MODE)
		os.chmod(env.tmpdir(), TMP_DIR_MODE)
		self.copySolutionFiles(env.tmpdir())

		# If the checks take too much time we have to keep the connection
		# alive through printing something.
		# misc.start_keepalive_thread()
		# well lets try without that first
		
		try:
			# dump variants file to allow processing in external checkers
#			try:
#				task_variant = task.hash(user.id())
#				file = os.path.join(new_tmpdir, "VARIANT")
#				f = open(file, "w")
#				f.write(`int(task_variant)`)
#				f.close()
#				os.chmod(file, Page.ZIP_MODE)
#			except IOError:
#				os.system("echo '<pre>'; whoami; ls -laR /praktomat/sandbox/tmp; echo '</pre>'")
#				print "<p><strong>Error dumping Variant file!</strong><br>"
#				traceback.print_exc(file=sys.stdout)
#				print "</pre>"
#				pass
			
			self.run_checks(env, verbose, run_secret)
		finally: 
			# awesome: this does actualy nothing. I guess the tempdir should be deleted?
			try:
				pass
				#self.remove(env.tmpdir())
			except IOError:
				pass
		
		# reset default temp dir location 
		tempfile.tempdir = None

		#misc.stop_keepalive_thread()

		# The set of sources may have changed while saving (and unpacking)
		# self.set_sources(env.sources())
	
	def run_checks(self, env, verbose, run_all): # , task
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
						task.diffchecker_set.all(),
						task.interfacechecker_set.all(),
						task.linewidthchecker_set.all(),
						task.textchecker_set.all(),
						task.cxxbuilder_set.all(),
						task.cbuilder_set.all(),
						task.anonymitychecker_set.all(),
						task.javabuilder_set.all(),
						task.dejagnutester_set.all() ]
		
		
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
	

class SolutionFile(models.Model):
	"""docstring for SolutionFile"""

	from django.core.files.storage import FileSystemStorage
	fs = FileSystemStorage(location=settings.SOLUTION_SANDBOX)
	
	def _get_upload_path(instance, filename):
		"""docstring for filePath"""
		solution = instance.solution
		return solution.author.username + '/'+ unicode(solution.task.id) + '/' + unicode(solution.id) + '/' + filename
	
	solution = models.ForeignKey(Solution)
	file = models.FileField(upload_to = _get_upload_path, storage=fs) 
	
	def __unicode__(self):
		return self.file.name.rpartition('/')[2]
		
	def content(self):
		"""docstring for content"""
		return unicode(self.file.read()) 
		
	def copyTo(self,directory):
		""" Copies this file to the given directory """
		shutil.copy(settings.SOLUTION_SANDBOX + "/" + self.file.name, directory)
		

