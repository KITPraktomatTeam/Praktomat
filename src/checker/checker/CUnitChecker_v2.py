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

from checker.checker.CreateFileChecker import CheckerWithFile
from checker.compiler.CBuilder import CBuilder
from checker.compiler.CXXBuilder import CXXBuilder


RXFAIL	   = re.compile(r"^(.*)(FAILURES!!!|your program crashed|cpu time limit exceeded|ABBRUCH DURCH ZEITUEBERSCHREITUNG|Could not find class|Killed|failures)(.*)$",	re.MULTILINE)

class IgnoringCBuilder2(CBuilder):
	_ignore = []

	def __init__(self,_flags, _ignore, _file_pattern,_output_flags):
		super(IgnoringCBuilder2,self).__init__(_flags=_flags, _file_pattern=_file_pattern, _output_flags=_output_flags)
		self._ignore=_ignore

	def get_file_names(self,env):
		rxarg = re.compile(self.rxarg())
		return [name for (name,content) in env.sources() if rxarg.match(name) and (not name in self._ignore)]

	# Since this checkers instances  will not be saved(), we don't save their results, either
	def create_result(self, env):
		assert isinstance(env.solution(), Solution)
		return CheckerResult(checker=self, solution=env.solution())


class IgnoringCXXBuilder2(CXXBuilder):
	_ignore = []

	def get_file_names(self,env):
		rxarg = re.compile(self.rxarg())
		return [name for (name,content) in env.sources() if rxarg.match(name) and (not name in self._ignore)]

	# Since this checkers instances  will not be saved(), we don't save their results, either
	def create_result(self, env):
		assert isinstance(env.solution(), Solution)
		return CheckerResult(checker=self, solution=env.solution())



class CUnitChecker2(CheckerWithFile):
	""" New Checker for CUnit and CPPUnit Unittests """ # code based upon JUnitChecker
# https://sourceforge.net/projects/cunit/
# https://sourceforge.net/projects/cppunit/
	# Add fields to configure checker instances. You can use any of the Django fields. (See online documentation)
	# The fields created, task, public, required and always will be inherited from the abstract base class Checker
	class_name = models.CharField(
            max_length=100,
            help_text=_("The fully qualified name of the test case executable (with fileending like .exe or .out)"),
    	    verbose_name=_("TestApp Filename")
	)
	test_description = models.TextField(help_text = _("Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded."))
	name = models.CharField(max_length=100, help_text=_("Name of the Testcase. To be displayed as title on Checker Results page"))
	_ignore = models.CharField(max_length=4096, help_text=_("Regular Expression for ignoring files while compile and link test-code.")+" Play with  RegEx at <a href=\"http://pythex.org/\" target=\"_blank\">http://pythex.org/ </a>",default="", blank=True)
	_ignore_sol = models.CharField(max_length=4096, help_text=_("Regular Expression for ignoring files while compile and link solution-code."),default="", blank=True)
        _flags = models.CharField(max_length = 1000, blank = True, default="-Wall -Wextra", help_text = _('Compiler flags'))
        _libs  = models.CharField(max_length = 1000, blank = True, default = "", help_text = _('Compiler libraries except cunit, cppunit'))
	
	LINK_CHOICES = (
	  ('o', u'Link Trainers Test-Code with solution objects (*.o)'),
	  ('so', u'Link solution objects as shared object (*.so, *.dll)'),
	  ('out', u'Link solution objects as seperate executable program (*.out, *.exe)'),
	)
	link_type = models.CharField(max_length=16, choices=LINK_CHOICES,default="o", help_text = _('How to use solution submission in test-code?'))


	CUNIT_CHOICES = (
	  ('cunit', u'CUnit 2.1-3'),
	  ('cppunit', u'CppUnit 1.12.1'),
	  ('c', u'C tests'),
	  ('cpp', u'CPP tests'),
	)
	cunit_version = models.CharField(max_length=16, choices=CUNIT_CHOICES,default="cunit")

	def use_cppBuilder(self):
		if 'pp' in self.cunit_version:
			return True
		else:
			return False
	
	def get_libs(self):
		if (('cunit' == self.cunit_version) or ('cppunit' == self.cunit_version)):
			return self._libs + ' -l'+ self.cunit_version
		return self._libs

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

	def clean(self):
		#call parents clean
		super(CUnitChecker2, self).clean()
		

	def run(self, env):
	# Robert Hartmann : 9.1.2018
	# okay lets play with an Idea:
	# We want to check students solutions 
	# 	- functions: input / output parameters
	# 	- functions: with return values
	# 	- programs: user interaction (input/output) 
	#         via STDOUT, STDERR, STDIN
	# In C we can only have one main function 
	# (unlike in Java there can a 
	# public static void main(String args) method 
	# in each class.)
	# => If the student have to write a program, 
	#    that is when the students submission contains a main function,
	#    than we cannot link student-code and test-code 
	#    to one binary executable. 
	#    In that case the student-code should 
	#	- compile and link as an executable program
	#	- compile as a shared object (*.so or *.dll)
	#    a) And the test-code should use that Library for testing functions: 
	#       on posix-systems use dlopen, dlsym, dlclose
	#          (Our Praktomat is a linux server)
	#       on windows it would be LoadLibrary, GetProcAdress, FreeLibrary.
	#    - but on Windows there must be a library-entry function for each *.dll
	#	BOOLEAN WINAPI DllMain( 
	#	IN HINSTANCE hDllHandle, 
	#	IN DWORD     nReason, 
	#	IN LPVOID    Reserved ) https://msdn.microsoft.com/de-de/library/windows/desktop/aa370448
	#    b) To test programs user interaction
	#	our test-code have to redirect STDOUT, STDERR, STDIN
	#	befor starting the new process with redirections
	#	on posix-systems use fork, execvp, 
	#	on windows CreatePipe, CreateProcess , see  https://msdn.microsoft.com/en-us/library/windows/desktop/ms682499(v=vs.85).aspx

		

		# first copy testfiles to sandbox
		noUnitTestSources = env.sources()
		copyTestFileArchive_result = super(CUnitChecker2,self).run_file(env) # Instance of Class CheckerResult in basemodel.py

		# if copying failed we can stop right here!
		if not copyTestFileArchive_result.passed:
			#result = self.create_result(env)
			result = copyTestFileArchive_result
			result.set_passed(False)
			result.set_log( #escape(self.CUNIT_CHOICES[self.cunit_version])   
    					""+ '<pre>' 
                                        + escape(self.test_description) 
                                        + '\n\n======== Preprocessing: Filecopy Failure-Results: ======\n\n</pre><br/>\n'
                                        + copyTestFileArchive_result.log )
			#raise TypeError
			return result
			
		result = copyTestFileArchive_result
	
		# now we configure build and link steps for test-code and solution-code
		
		
		# link_type: o, so, out
		test_builder = None
		solution_builder = None

		# if link_type is o, we have to compile and link all code with test_builder
		if "o" == self.link_type:

			#languageCompiler C or CPP 
			if self.use_cppBuilder():
				#CPP
				#test_builder = IgnoringCXXBuilder2(_flags=self._flags, _libs=self.get_libs() ,_file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags="-o "+self.class_name)
				test_builder = IgnoringCXXBuilder2(_flags=self._flags ,_file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags="-o "+self.class_name)
			else:
				#C
				test_builder = IgnoringCBuilder2(_flags=self._flags ,_file_pattern=r"^.*\.(c|C)$",_output_flags="-o "+self.class_name)
		else:
			#ignoring all test-code filenames for solution_builder
			#ignoring all non test-code filenames for test_builder
			
			#TODO: How we can get the names?
			import zipfile  #via src/utilities/file_operations
			# ZipFile.namelist()	Return a list of archive members by name.		
			
			try:
				with zipfile.ZipFile(self.file.path()) as zip_file:
					names = zip_file.namelist()
			except zipfile.BadZipfile:
					names = [self.file]
			 
			raise TypeError
			# shared object or executable
			if "so" == self.link_type: 
				#languageCompiler C or CPP 
				if self.use_cppBuilder():
					#CPP
					#solution_builder = IgnoringCXXBuilder2(_flags=self._flags, _libs=self.get_libs() ,_file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags="-shared -fPIC -o "+env.program()+".so",_main_required=True)
					solution_builder = IgnoringCXXBuilder2(_flags=self._flags, _ignore=names, _file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags="-shared -fPIC -o "+env.program()+".so")
					test_builder = IgnoringCXXBuilder2(_flags=self._flags, _ignore=noUnitTestSources, _file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags="-o "+self.class_name)
					#test_builder = IgnoringCXXBuilder2(_flags=self._flags,_file_pattern=names,_output_flags="-o "+self.class_name)
				else:
					#C
					solution_builder = IgnoringCBuilder2(_flags=self._flags, _ignore=names, _file_pattern=r"^.*\.(c|C)$",_output_flags="-shared -fPIC -o "+env.program()+".so")
					test_builder = IgnoringCBuilder2(_flags=self._flags, _ignore=noUnitTestSources, _file_pattern=r"^.*\.(c|C)$",_output_flags="-o "+self.class_name)
			else: #executable
				#languageCompiler C or CPP 
				if self.use_cppBuilder():
					#CPP
					solution_builder = IgnoringCXXBuilder2(_flags=self._flags, _ignore=names ,_file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags="-o "+env.program()+".out")
					test_builder = IgnoringCXXBuilder2(_flags=self._flags, _ignore=noUnitTestSources, _file_pattern=r"^.*\.(c|C)$",_output_flags="-o "+self.class_name)
				else:
					#C
					solution_builder = IgnoringCBuilder2(_flags=self._flags, _ignore=names , _file_pattern=r"^.*\.(c|C)$",_output_flags="-o "+env.program()+".out")
					test_builder = IgnoringCBuilder2(_flags=self._flags ,_ignore=noUnitTestSources, _file_pattern=r"^.*\.(c|C)$",_output_flags="-o "+self.class_name)
		
		build_solution_result = None
		if solution_builder:
			build_solution_result = solution_builder.run(env)
			if not build_solution_result.passed:
				# result = self.create_result(env)
				# result += build_solution_result
				result.set_passed(False)
				result.set_log( '<pre>' + escape(self.test_description) + '\n\n==========  Preprocessing =============\n*    Generating "Shared Object"       *\n* or "Executable" from solution files *\n======== Failure-Results ==============\n\n</pre><br/>\n'+build_solution_result.log )
				# raise TypeError
				return result
		#result = build_solution_result

		build_test_result = test_builder.run(env) 
		if not build_test_result.passed:
			# result = self.create_result(env)
			# result += build_test_result
			result.set_passed(False)
			result.set_log( escape(self.cunit_version)  + '<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/>\n'+build_test_result.log )
			# raise TypeError
			return result
		#result = build_test_result

		environ = {}

		environ['UPLOAD_ROOT'] = settings.UPLOAD_ROOT
		#environ['JAVA'] = settings.JVM
                script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'scripts')
		#environ['POLICY'] = os.path.join(script_dir,"junit.policy")

		#cmd = [u'echo ',self.class_name, u'&&' , self.runner(), self.class_name]
		cmd = [os.path.join(script_dir,self.runner()),self.class_name]
		[output, error, exitcode,timed_out, oom_ed] = execute_arglist(cmd, env.tmpdir(),environment_variables=environ,timeout=settings.TEST_TIMEOUT,fileseeklimit=settings.TEST_MAXFILESIZE, extradirs=[script_dir])

		#result = self.create_result(env)

		(output,truncated) = truncated_log(output)
		output = '<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/><pre>' + escape(output) + '</pre>'


		result.set_log(output,timed_out=timed_out or oom_ed,truncated=truncated,oom_ed=oom_ed)
		result.set_passed(not exitcode and not timed_out and not oom_ed and self.output_ok(output) and not truncated)
		result.save()
		return result

#class JUnitCheckerForm(AlwaysChangedModelForm):
#	def __init__(self, **args):
#		""" override default values for the model fields """
#		super(JUnitCheckerForm, self).__init__(**args)
#		self.fields["_flags"].initial = ""
#		self.fields["_output_flags"].initial = ""
#		self.fields["_libs"].initial = "junit3"
#		self.fields["_file_pattern"].initial = r"^.*\.[jJ][aA][vV][aA]$"
	
class CUnitChecker2Inline(CheckerInline):
	""" This Class defines how the the the checker is represented as inline in the task admin page. """
	model = CUnitChecker2
	verbose_name = "C/C++ Unit Checker 2"
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

	
