# -*- coding: utf-8 -*-

from pipes import quote
import re, subprocess
import string
from django.db import models
from django.utils.translation import ugettext_lazy as _


from checker.models import Checker, CheckerResult, execute

class Builder(Checker):
	""" Build a program. This contains the general infrastructure to build a program with a compiler.  Specialized subclass are provided for different languages and compilers. """

	class Meta(Checker.Meta):
		abstract = True
	
	# builder configuration. override in subclass
	_compiler				= "gcc"						# command to invoce the compiler in the shell
	_language				= "konfigurierbar"			# the language of the compiler eg. C++ or Java
	_rx_warnings			= r"^([^:]*:[^:].*)$"		# Regular expression describing warings and errors in the output of the compiler
	_env                            = {}
	
			
	_flags			= models.CharField(max_length = 1000, blank = True, default="-Wall", help_text = _('Compiler flags'))
	_output_flags	= models.CharField(max_length = 1000, blank = True, default ="-o %s", help_text = _('Output flags. \'%s\' will be replaced by the program name.'))
	_libs			= models.CharField(max_length = 1000, blank = True, default = "", help_text = _('Compiler libraries'))
	_file_pattern	= models.CharField(max_length = 1000, default = r"^[a-zA-Z0-9_]*$", help_text = _('Regular expression describing all source files to be passed to the compiler.'))
	
	def title(self):
		return u"%s - Compiler" % self.language()

	@staticmethod
	def description():
		return u"Diese Prüfung ist bestanden, wenn der Compiler das Programm ohne Fehler oder Warnungen übersetzt."

	def compiler(self):
		""" Compiler name. To be overloaded in subclasses. """
		return self._compiler

	def flags(self, env):
		""" Compiler flags.	To be overloaded in subclasses. """
		return self._flags.split(" ")

	def output_flags(self, env):
		""" Output flags """
		try:
			return (self._output_flags % env.program()).split(" ")
		except:
			return self._output_flags.split(" ")

	def libs(self):
		""" Compiler libraries.	 To be overloaded in subclasses. """
		return self._libs.split(" ")

	def environment(self):
		""" Environment to be set on onvocation of Compiler. """
		return self._env

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

	class NotFoundError(Exception):
			def __init__(self, description):
				self.description = description
			def __str__(self):
				return self.description
	
	def main_module(self, env):
		""" Creates the name of the main module from the (first) source file name. """
		for module_name in self.get_file_names(env):
			try:
				return module_name[:string.index(module_name, '.')]
			except ValueError:
				pass
		# Module name not found

		raise self.NotFoundError("The main module could not be found.\n")

	def run(self, env):
		""" Build it. """
		result = CheckerResult(checker=self)

		try:
			env.set_program(self.main_module(env))
		except self.NotFoundError as e:
			result.set_log(e)
			result.set_passed(False)
			return result
		
		filenames = [quote(name) for name in self.get_file_names(env)]
		args = [self.compiler()] + self.output_flags(env) + self.flags(env) + filenames + self.libs()
		output = execute(args, env.tmpdir(),self.environment())[0]
		output = self.enhance_output(env, output)
		
		# Allow server to delete created subfolders
		execute('chmod -R 0777 *', env.tmpdir())		

		# The executable has to exist and we mustn't have any warnings.
		passed = not self.has_warnings(output)	
		result.set_log(self.build_log(output,args,set(filenames).intersection([quote(solutionfile.path()) for solutionfile in env.solution().solutionfile_set.all()])))
		result.set_passed(passed)
		return result

	def build_log(self,output,args,filenames):
		return	"<pre>" + output + "</pre>" if output else ""
