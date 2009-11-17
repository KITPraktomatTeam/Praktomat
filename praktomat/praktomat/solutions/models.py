# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from praktomat.tasks.models import Task
from django.utils.translation import ugettext_lazy as _

import os, re, tempfile, shutil
 


class Solution(models.Model):
	"""docstring for Solution"""
	
	task = models.ForeignKey(Task)
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
	
	def check(self, run_secret = 0): #task, user, key, course_id,
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
		#if self.tab_width() > 0:				# unsure about that
		#	env.set_tab_width(self.tab_width())
		env.set_user(self.author)
		# env.set_key(key)						# what is the key?
		# env.set_course_id(course_id)			
		# env.set_task_id(self.task_id())		# set task insted of id
		
		try:
			# Setting default temp dir location and creating it
			tempfile.tempdir = os.path.join(settings.MEDIA_ROOT, "SolutionSandbox")
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
			try:
				pass
				#shutil.rmtree(new_tmpdir)
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
						task.anonymitychecker_set.all(),
						task.javabuilder_set.all(),
						task.javagccbuilder_set.all(),
						task.fortranbuilder_set.all(),
						task.dejagnusetup_set.all(), 
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
	
	def _get_upload_path(instance, filename):
		solution = instance.solution
		return 'SolutionArchive/Task_' + unicode(solution.task.id) + '/User_' + solution.author.username + '/Solution_' + unicode(solution.id) + '/' + filename
	
	solution = models.ForeignKey(Solution)
	file = models.FileField(upload_to = _get_upload_path) 
	# File mime content types allowed to upload
	supported_types_re = re.compile(r'^(text/.*|application/octet-stream)$')
	# Ignore hidden and OS-specific files in zipfiles
	# .filename or __MACOSX/bla.txt or /rootdir or ..dirup
	ignorred_file_names_re = re.compile('^(\..*|__MACOSX/.*|/.*|\.\..*)$')
	
	
	def __unicode__(self):
		return self.file.name.rpartition('/')[2]
		
	def content(self):
		"""docstring for content"""
		try:
			return unicode(self.file.read(), 'latin-1') 
		except:
			return _("File couldn't be encoded.")
		
	def copyTo(self,directory):
		""" Copies this file to the given directory """
		shutil.copy(self.file.path, directory)
		

