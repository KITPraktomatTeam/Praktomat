# -*- coding: utf-8 -*-

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker, CheckerResult, CheckerFileField, truncated_log
from checker.admin import	CheckerInline, AlwaysChangedModelForm
from utilities.safeexec import execute_arglist
from utilities.file_operations import *
from solutions.models import Solution

from checker.compiler.CBuilder import CBuilder
from checker.compiler.CXXBuilder import CXXBuilder

import logging
import os
from string import Template


RXFAIL	   = re.compile(r"^(.*)(FAILURES!!!|your program crashed|cpu time limit exceeded|ABBRUCH DURCH ZEITUEBERSCHREITUNG|Could not find class|Killed|failures)(.*)$",	re.MULTILINE)

class IgnoringCBuilder(CBuilder):
	_ignore = []

	def get_file_names(self,env):
		rxarg = re.compile(self.rxarg())
                return [name for (name,content) in env.sources() if rxarg.match(name) and (not name in self._ignore)]

	# Since this checkers instances  will not be saved(), we don't save their results, either
	def create_result(self, env):
		assert isinstance(env.solution(), Solution)
		return CheckerResult(checker=self, solution=env.solution())


class IgnoringCXXBuilder(CXXBuilder):
	_ignore = []

	def get_file_names(self,env):
		rxarg = re.compile(self.rxarg())
		return [name for (name,content) in env.sources() if rxarg.match(name) and (not name in self._ignore)]

	# Since this checkers instances  will not be saved(), we don't save their results, either
	def create_result(self, env):
		assert isinstance(env.solution(), Solution)
		return CheckerResult(checker=self, solution=env.solution())



class CUnitChecker(Checker):
	""" New Checker for CUnit and CPPUnit Unittests. based upon JUnitChecker """
# https://sourceforge.net/projects/cunit/
# https://sourceforge.net/projects/cppunit/
	# Add fields to configure checker instances. You can use any of the Django fields. (See online documentation)
	# The fields created, task, public, required and always will be inherited from the abstract base class Checker
	class_name = models.CharField(
            max_length=100,
            help_text=_("The fully qualified name of the test case executable (with fileending like .exe or .out)")
        )
	test_description = models.TextField(help_text = _("Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded."))
	name = models.CharField(max_length=100, help_text=_("Name of the Testcase. To be displayed as title on Checker Results page"))
	ignore = models.CharField(max_length=4096, help_text=_("space-seperated list of files to be ignored during compilation, i.e.: these files will not be compiled."),default="", blank=True)
        _flags = models.CharField(max_length = 1000, blank = True, default="-Wall -Wextra", help_text = _('Compiler flags'))
        _libs  = models.CharField(max_length = 1000, blank = True, default = "", help_text = _('Compiler libraries except cunit, cppunit'))


        TPL_TESTRESULT = Template('<pre>$description' + \
                                  '\n\n======== Test Results ======\n\n' + \
                                  '</pre><br/>' + \
                                  '<pre>$output</pre>')
        
	CUNIT_CHOICES = (
	  ('cunit', u'CUnit 2.1-3'),
	  ('cppunit', u'CppUnit 1.12.1'),
	)
	cunit_version = models.CharField(max_length=16, choices=CUNIT_CHOICES,default="cunit")

                
	def runner(self):
		#return {'cunit' : 'cuMain.exe', 'cppunit' : 'cxxMain.exe' }[self.cunit_version]
		# cTestrunner is name of shell-script file inside folder checker/scripts 
		return "cTestrunner"

	def title(self):
		return u"C/Cpp Unit Test: " + self.name

	@staticmethod
	def description():
		return u"This Checker runs a C/Cpp Unit Testcases existing in the sandbox. You may want to use CreateFile Checker to create CUnit .c/.cpp and possibly input data files in the sandbox before running the C/CxxBuilder. Unit tests will only be able to read input data files if they are placed in the work/ subdirectory."

	def output_ok(self, output):
		return (RXFAIL.search(output) == None)

	def run(self, env):
                                
                LOGGER = logging.getLogger()
                fmt = logging.Formatter('%(asctime)s [%(process)d] [%(levelname)s] %(funcName)s: %(message)s')

                if len(LOGGER.handlers) == 0:
                        handler = logging.FileHandler("/tmp/hmw.log",
                                                      encoding="utf-8")
                        handler.setFormatter(fmt)
                        LOGGER.addHandler(handler)
                        LOGGER.setLevel(logging.DEBUG)
                LOGGER.info("Starting")

                
		c_builder = None

                # First let us compile all files to object code
		if "cunit" == self.cunit_version:
			c_builder = IgnoringCBuilder(_file_pattern=r"^.*\.(c|C)$")
		else:
			c_builder = IgnoringCXXBuilder(_file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$")

                c_builder._flags = self._flags
                c_builder._libs = self._libs
                c_builder._output_flags = ""
                c_builder._main_required = False
		c_builder._ignore = self.ignore.split(" ")
              
		build_result = c_builder.run(env)
                              
		if not build_result.passed:
			result = self.create_result(env)
                        
			result.set_passed(False)              
                        result.set_log(self.TPL_TESTRESULT.substitute(
                                description=escape(self.test_description),
                                output=build_result.log))

			return result

		environ = {}
                

                # Next let's shell out and dress all object files
                # to our needs.
                script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'scripts')
                cmd = [os.path.join(script_dir, "dressObjects"),
                       self.class_name]
		[output, error, exitcode, timed_out, oom_ed] = execute_arglist(cmd, env.tmpdir(), environment_variables=environ, timeout=settings.TEST_TIMEOUT, fileseeklimit=settings.TEST_MAXFILESIZE, extradirs=[script_dir])


                passed = not exitcode \
                         and not timed_out \
                         and not oom_ed \
                         and self.output_ok(output)

                if not passed:
                        result = self.create_result(env)

			result.set_passed(passed)

		        (output, truncated) = truncated_log(output)

                        output = self.TPL_TESTRESULT.substitute(
                                description=escape(self.test_description),
                                output=escape(output))

		        result.set_log(output,
                                       timed_out=timed_out or oom_ed,
                                       truncated=truncated,
                                       oom_ed=oom_ed)

                        return result
                        
                
                # Get all object files of this run...
                tmp = re.compile('^(.*\.)c')
                flist = [tmp.sub(r"\1o", name)\
                         for (name,void) in env.sources()\
                         if name.endswith('.c')]

                for f in flist:
                        try:
                                for (name, void) in env.sources():
                                        if f == name: raise StopIteration
                                env.add_source(f, None)
                        except StopIteration: pass
                        
                
                # ... and link them all into the unit test binary.
                c_builder = IgnoringCBuilder(_flags=self._flags,
                                             _libs='-l'+self.cunit_version+' '+self._libs,
                                             _file_pattern=r"^.*\.o$",
                                             _output_flags="-o "+self.class_name,
                                             _main_required=True)

                build_result = c_builder.run(env)

                
                if not build_result.passed:
			result = self.create_result(env)
			result.set_passed(False)

                        result.set_log(self.TPL_TESTRESULT.substitute(
                                description=escape(self.test_description),
                                output=build_result.log))

			return result

                
		environ['UPLOAD_ROOT'] = settings.UPLOAD_ROOT
                script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'scripts')

		cmd = [os.path.join(script_dir,self.runner()),
                       "@@",
                       self.class_name,
                       env.program()]
		[output, error, exitcode,timed_out, oom_ed] = execute_arglist(cmd, env.tmpdir(),environment_variables=environ,timeout=settings.TEST_TIMEOUT,fileseeklimit=settings.TEST_MAXFILESIZE, extradirs=[script_dir])

		result = self.create_result(env)

		(output,truncated) = truncated_log(output)
                output = self.TPL_TESTRESULT.substitute(
                        description=escape(self.test_description),
                        output=escape(output))

		result.set_log(output,
                               timed_out=timed_out or oom_ed,
                               truncated=truncated,
                               oom_ed=oom_ed)
                
		result.set_passed(not exitcode \
                                  and not timed_out
                                  and not oom_ed \
                                  and self.output_ok(output) \
                                  and not truncated)
		return result

#class JUnitCheckerForm(AlwaysChangedModelForm):
#	def __init__(self, **args):
#		""" override default values for the model fields """
#		super(JUnitCheckerForm, self).__init__(**args)
#		self.fields["_flags"].initial = ""
#		self.fields["_output_flags"].initial = ""
#		self.fields["_libs"].initial = "junit3"
#		self.fields["_file_pattern"].initial = r"^.*\.[jJ][aA][vV][aA]$"
	
class CBuilderInline(CheckerInline):
	""" This Class defines how the the the checker is represented as inline in the task admin page. """
	model = CUnitChecker
	verbose_name = "C/C++ Unit Checker"
#	form = JUnitCheckerForm

# A more advanced example: By overwriting the form of the checkerinline the initial values of the inherited atributes can be overritten.
# An other example would be to validate the inputfields in the form. (See Django documentation)
#class ExampleForm(AlwaysChangedModelForm):
	#def __init__(self, **args):
		#""" override public and required """
		#super(ExampleForm, self).__init__(**args)
		#self.fields["public"].initial = False
		#self.fields["required"].initial = False

#class ExampleCheckerInline(CheckerInline):
	#model = ExampleChecker
	#form = ExampleForm

	
