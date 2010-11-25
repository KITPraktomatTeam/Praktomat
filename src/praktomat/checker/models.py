# -*- coding: utf-8 -*-
from os import *
from os.path import *
import subprocess
from django.conf import settings
from django.db import models
from praktomat.tasks.models import Task
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

import string
	
def execute(command, working_directory, environment_variables={}):
	""" Wrapper to execute Commands with the praktomat testuser. """
	if isinstance(command, list):
		command = ' '.join(command)
	script = join(join(dirname(__file__),'scripts'),'execute')
	command = script + ' ' + command
	environment = environ
	environment.update(environment_variables)
	if (settings.USEPRAKTOMATTESTER): environment['USEPRAKTOMATTESTER'] = 'TRUE'
	[output, error] = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=working_directory, env=environment, shell=True).communicate()
	return [output, error]


class Checker(models.Model):
	""" A Checker implements some quality assurance.
	 
	A Checker has three indicators:
		1. It is *public* - the results are presented to the user
It is *required* - it must be passed for submission
		3. It is run .

	If a Checker is not run always, it is only run if a *task_maker*
	starts the complete rerun of all Checkers. """

	created = models.DateTimeField(auto_now_add=True)
	
	task = models.ForeignKey(Task)
	
	public = models.BooleanField(default=True, help_text = _('Test results are displayed to the submitter.'))
	required = models.BooleanField(default=False, help_text = _('The test must be passed to submit the solution.'))
	always = models.BooleanField(default=True, help_text = _('The test will run on submission time.'))
	
	class Meta:
		abstract = True
		app_label = 'checker'
		
	def __unicode__(self):
		return self.title()

	def result(self):
		""" Creates a new result.
		May be overloaded by subclasses."""
		return CheckerResult(checker=self)
		
	def run(self, env):
		""" Runs tests in a special environment.
		Returns a CheckerResult. """
		assert isinstance(env, CheckerEnvironment)
		return self.result()

	def title(self):
		""" Returns the title for this checker category. To be overloaded in subclasses. """
		return u"Prüfung"

	def requires(self):
		""" Returns the list of passed Checkers required by this checker.
		Overloaded by subclasses. """ 
		return []		
			   			
class CheckerEnvironment:
	""" The environment for running a checker. """

	def __init__(self):
		""" Constructor: Creates a standard environment. """
		self._tmpdir = None  # Temporary build directory
		self._program = None # Executable program
		self._sources = []   # Sources as [(name, content)...]
		self._source = None
		self._user = None	# Submitter of this program
		self._key  = None	# Key of the submitter
		self._course_id = "" # Course of the submitter
		self._tab_width = 4  # Tab width
		self._task_id = None # Identifier of the task/solution to be solved

	def tmpdir(self):
		""" Returns the path name of temporary build directory. """
		return self._tmpdir

	def program(self):
		""" Returns the name of the executable program. """
		return self._program

	def sources(self):
		""" Returns the list of source files. """
		return self._sources

	def user(self):
		""" Returns the submitter of this program (class User). """
		return self._user

	def key(self): # What is the Key ?????????
		""" Returns the key of the submitter. """
		return self._key

	def course_id(self):
		""" Returns the course identifier of the submitter. """
		return self._course_id

	def tab_width(self): # Whats that needed for ????
		""" Returns the tab width the submitter chose. """
		return self._tab_width

	def task_id(self): # shoudn't the checker know?
		""" Returns the task id of the submitter. """
		return self._task_id

	def set_tmpdir(self, tmpdir):
		""" Sets the path name of the temporary build directory. """
		assert isinstance(tmpdir, str)
		self._tmpdir = tmpdir
	
	def set_program(self, program):
		""" Sets the name of the executable program. """
		#assert isinstance(program, str)
		self._program = program

	def set_sources(self, sources):
		"""  Sets the list of source file names. """
		assert isinstance(sources, list)
		self._sources = sources
		
	def set_user(self, user):
		""" Sets the submitter (class User). """
		#assert isinstance(user, User.User)
		self._user = user

	def set_key(self, key):
		""" Sets the key of the submitter. """
		#assert isinstance(key, long)
		self._key = key

	def set_course_id(self, course_id):
		""" Sets the course identifier of the submitter. """
		assert isinstance(course_id, str)
		self._course_id = course_id

	def set_tab_width(self, tab_width):
		""" Sets the tab witdh of the sources. """
		assert isinstance(tab_width, int)
		self._tab_width = tab_width

	def set_task_id(self, task_id):
		""" Sets task identifier of the submitter. """
		assert isinstance(task_id, str)
		self._task_id = task_id

		
class CheckerResult(models.Model):
	""" A CheckerResult returns the result of a Checker.
	It contains:
		- A flag that indicates if the check passed.
		- A flag that indicates if the check is *required* to pass.
		- A flag that indicates it the check is *public*.
		- The title of the check.
		- The log of the run.
		- The time of the run. """
	
	from praktomat.solutions.models import Solution
	solution = models.ForeignKey(Solution)
	content_type = models.ForeignKey(ContentType) 
	object_id = models.PositiveIntegerField() 
	checker = generic.GenericForeignKey('content_type','object_id') 
	
	passed = models.BooleanField(default=True,  help_text=_('Indicates whether the test has been passed'))
	log = models.TextField(help_text=_('Text result of the checker'))
	creation_date = models.DateTimeField(auto_now_add=True)
	
	def title(self):
		""" Returns the title of the Checker that did run. """
		return self.checker.title()

	def required(self):
		""" Checks if the Checker is *required* to be passed. """
		return self.checker.required

	def public(self):
		""" Checks if the results of the Checker are *public*. """
		return self.checker.public

	def set_log(self, log):
		""" Sets the log of the Checker run. """
		self.log = log

	def set_passed(self, passed):
		""" Sets the passing state of the Checker. """
		assert isinstance(passed, int)
		self.passed = passed

