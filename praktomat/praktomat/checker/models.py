# -*- coding: utf-8 -*-

from django.db import models
from praktomat.tasks.models import Task
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import os
import re
import subprocess
import string
	
# Mode for temporary directories.
TMP_DIR_MODE = 0770

# Maximal size of test output read
MAX_OUTPUT = 1000000


class Checker(models.Model):
	""" A Checker implements some quality assurance.
	 
	A Checker has three indicators:
		1. It is *public* - the results are presented to the user
		2. It is *required* - it must be passed for submission
		3. It is run *always* - it is run before submission.

	If a Checker is not run always, it is only run if a *task_maker*
	starts the complete rerun of all Checkers. """

	created = models.DateTimeField(auto_now_add=True)
	
	task = models.ForeignKey(Task)
	
	public = models.BooleanField(default=True, help_text = _('Test results are displayed to the submitter.'))
	required = models.BooleanField(default=True, help_text = _('The test must be passed to submit the solution.'))
	always = models.BooleanField(default=True, help_text = _('The test will run on submission time.'))					# Misleading name?
	
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
		
	#def task(self): # untestet
	#	return self.proxy.task

	def requires(self):
		""" Returns the list of passed Checkers required by this checker.
		Overloaded by subclasses. """ 
		return []

#	def description(self):
#		""" Returns a description for this Checker.
#		Overloaded by subclasses. """
#		pass		
			   			

#		
#	def htmlize_output(self, log, env): # no not here! --------------------------------------------------------
#		""" Prepares the output for presentation.
#		Includes cleanup and highlighting. """
#		# Clean the output
#		# MIGRATION 4.0.20
#		try:
#			if self._rxremove:
#				log = re.sub(self._rxremove, "", log)
#		except:
#			pass
#		# HTMLize it all
#		log = htmlize(log)
#		for (name, content) in env.sources():
#			log = string.replace(log, name,"<A HREF=\\"#" + `env.key()` + name \\ + "\\">" + name + "</A>")
#		
#		# Every line that contains a failure message is to be enhanced.
#		return (re.sub(RXFAIL, r"\\1<B><FONT COLOR=" + FAIL_COLOR + ">" +	r"\\2</FONT></B>\\3",	log))


class Builder(Checker):
	""" Build a program.
	This contains the general infrastructure to build a programm with a
	compiler.  Specialized subclass are provided for different languages
	and compilers. """

	class Meta(Checker.Meta):
		abstract = True
	
	# builder configuration. override in subclass
	_compiler				= "gcc"						# command to invoce the compiler in the shell
	_language				= "konfigurierbar"			# the language of the compiler eg. C++ or Java
	_rx_warnings			= r"^([^ :]*:[^:].*)$"		# Regular expression describing warings and errors in the output of the compiler
	
# Sadly this had to go into the subclass because of non overrideable defaults
	# default values for the model fields
#	global defaults
#	defaults = {
#		'flags'			: "-Wall", # -static"
#		'output_flags'	: "-o %s",
#		'libs'			: "",
#		'file_pattern'	: r"^[a-zA-Z0-9_]*$"			# Regular expression describing all source files to be passed to the compiler.
#	}
	
#	def default(key):
#		""" By making the model field defaults a callable instead of an value it will be called every time a new object is created wich will allow for altered defaults in subclasses. """
#		return defaults[key]
	
	
#	_flags			= models.CharField(max_length = 1000, blank = True, help_text = _('Compiler flags')) #default = default('flags'), 
#	_output_flags	= models.CharField(max_length = 1000, blank = True, default = default('output_flags'), help_text = _('Output flags. \'%s\' will be replaced by the program name.'))
#	_libs			= models.CharField(max_length = 1000, blank = True, default = default('libs'), help_text = _('Compiler libraries'))
#	_file_pattern	= models.CharField(max_length = 1000, default = default('file_pattern'), help_text = _('Regular expression describing all source files to be passed to the compiler.'))
	
	
	def title(self):
		return u"%s - Compiler" % self.language()
	   

	def description(self):
		return u"Diese Prüfung ist bestanden, wenn <EM> %s </EM> das Programm ohne Fehler oder Warnungen übersetzt." % self.compiler()

	def compiler(self):
		""" Compiler name. To be overloaded in subclasses. """
		return self._compiler

	def flags(self, env):
		""" Compiler flags.	To be overloaded in subclasses. """
		return self._flags

	def output_flags(self, env):
		""" Output flags """
		try:
			return self._output_flags % env.program()   # Is this needed?
		except:
			return self._output_flags

	def libs(self):
		""" Compiler libraries.	 To be overloaded in subclasses. """
		return self._libs

	def language(self):
		""" Language.  To be overloaded in subclasses """
		return self._language

	def rxarg(self):
		""" Regexp for compile command argument.  Files that do not match this regexp will be uploaded,
			but not passed as argument to the compiler 	(such as header files in C/C++).	
			This also protects somewhat against options (`-foo') and metacharacters (`foo; ls') in file names. To be overloaded in subclasses. """
		return self._file_pattern

	def get_file_names(self,env):
		rxarg = re.compile(self.rxarg())
		return [name for (name,content) in env.sources() if rxarg.match(name)]		
		

	def exec_file(self, tmpdir, program_name):
		""" File of the generated executable.  To be overloaded in subclasses. """
		return os.path.join(tmpdir, program_name)

	def enhance_output(self, env, output):
		""" Add more info to build output OUTPUT.  To be overloaded in subclasses. """
		return re.sub(re.compile(self._rx_warnings, re.MULTILINE), r"<b>\1</b>", output)
		
	def has_warnings(self, output):
		""" Return true if there are any warnings in OUTPUT """
		return re.compile(self._rx_warnings, re.MULTILINE).search(output) != None

	def result(self):
		return BuilderResult(self)

	def run(self, env):
		""" Build it. """
		env.set_program(env.main_module())

		result = CheckerResult(checker=self)
		#result.set_invocation(self.compile_command_invocation(env))

		#cmd = self.compile_command(env)
		
		# This propably needs a timeout ....
		# subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)
		args = [self.compiler(), self.output_flags(env), self.flags(env)] + self.get_file_names(env) + [self.libs()]
		args = [arg for arg in args if arg !=""] # trash ""s, cause they produce errors
		output = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=env.tmpdir()).communicate()[0] #executable = self.compiler(),
		output = self.enhance_output(env, output)
		#assert False
		# The executable has to exist and we mustn't have any warnings.
		passed = not self.has_warnings(output)	
		result.set_log("<pre>" + output + "</pre>")
		result.set_passed(passed)

		return result


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
	
#	def source_names_for_compiler(self):   Keine Virtuellen Quellen mehr und der name ist eh der basenname(oder?)
#		names = []
#		
#		for (name, content) in self._sources:
#			#FIX
#			name = os.path.basename(name)
#			names.append(name)
#				
#		for name in self._virtual_sources:
#			name = os.path.basename(name)
#			names.append(name)
#				
#		return names

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
	
	def set_program(self, program): # What?
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

	def main_module(self):
		""" Creates the name of the main module from the (first) source file name. """
		for (module_name, module_content) in self.sources():
			try:
				return module_name[:string.index(module_name, '.')]
			except:
				pass

		# Module name not found
		return None

		
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
	
#	def __unicode__(self):
		# Vorsicht: das geht ins Auge!
#		return unicode(self.solution) + ": " + unicode(self.checker)
	
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
		#assert isinstance(log, str)     Oder auch mal unicode
		self.log = log

	def set_passed(self, passed):
		""" Sets the passing state of the Checker. """
		assert isinstance(passed, int)
		self.passed = passed
	


#			if self.required():
#				print """<P><FONT COLOR=""" + FAIL_COLOR + """><STRONG>
#				Ihr Programm kann so nicht angenommen werden.
#				</STRONG></FONT> Bitte korrigieren Sie die oben
#				aufgef&uuml;hrten Probleme.</P>"""
#			else:
#				print """<P><FONT COLOR=""" + PASS_MOSTLY_COLOR + """><STRONG>
#				Ihr Programm hat einige Schw&auml;chen.
#				</STRONG></FONT> Diese Schw&auml;chen wirken sich
#				negativ in der Beurteilung aus. Wir empfehlen, die
#				oben aufgef&uuml;hrten Probleme zu korrigieren.</P>"""

