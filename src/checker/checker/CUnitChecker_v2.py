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


#TODO: okay perhaps we could merge both IgnoringBuilders while specialising from Compiler

class IgnoringCBuilder2(CBuilder):
	_ignore = []

	def __init__(self,_flags, _ignore, _file_pattern, _output_flags):
		super(IgnoringCBuilder2,self).__init__(_flags=_flags, _file_pattern=_file_pattern, _output_flags=_output_flags)
		self._ignore=_ignore

	def get_file_names(self,env):
		rxarg = re.compile(self.rxarg())
		ret = [name for (name,content) in env.sources() if rxarg.match(name) and (not name in self._ignore)]
		return ret

	def runFail(self,env,_fail):
		if _fail:
			raise TypeError
		return self.run(env)

	# Since this checkers instances  will not be saved(), we don't save their results, either
	def create_result(self, env):
		assert isinstance(env.solution(), Solution)
		return CheckerResult(checker=self, solution=env.solution())



class IgnoringCXXBuilder2(CXXBuilder):
	_ignore = []

	def __init__(self,_flags, _ignore, _file_pattern, _output_flags):
		super(IgnoringCXXBuilder2,self).__init__(_flags=_flags, _file_pattern=_file_pattern, _output_flags=_output_flags)
		self._ignore=_ignore

	def get_file_names(self,env):
		rxarg = re.compile(self.rxarg())
		ret = [name for (name,content) in env.sources() if rxarg.match(name) and (not name in self._ignore)]
		return ret

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
	_test_name = models.CharField(
            max_length=100,
            help_text=_("The fully qualified name of the test case executable (with fileending like .exe or .out)"),
    	    verbose_name=_("TestApp Filename"),
	    default=u"TestApp.out"
	)
	_test_ignore = models.CharField(max_length=4096, 
	    help_text=_("Regular Expression for ignoring files while compile and link test-code.")+" <br> Play with  RegEx at <a href=\"http://pythex.org/\" target=\"_blank\">http://pythex.org/ </a>",
	    default=u"sorry, this feature doesn't work now", blank=True)

	_test_flags = models.CharField(max_length = 1000, blank = True, 
	    default=u"-Wall -Wextra -Wl,--warn-common", 
	    help_text = _("Compiler and Linker flags for i.e. libraries used while generating TestApp. <br> Don't fill in cunit or cppunit here."))

	LINK_CHOICES = (
	  (u'o', u'Link Trainers Test-Code with solution objects (*.o)'),
	  (u'so', u'MUT: Link solution objects as shared object (*.so, *.dll)'),
	  (u'out', u'MUT: Link solution objects as seperate executable program (*.out, *.exe)'),
	)
	LINK_DICT = {u'out':u'-o' , u'so':u'-shared -fPIC -o' , u'o':u''}
	link_type = models.CharField(max_length=16, choices=LINK_CHOICES,default="o", help_text = _('How to use solution submission in test-code?'))
	

	CUNIT_CHOICES = (
	  ('cunit', u'CUnit 2.1-3'),
	  ('cppunit', u'CppUnit 1.12.1'),
	  ('c', u'C tests'),
	  ('cpp', u'CPP tests'),
	)
	CUNIT_DICT = {u'cunit':u'-lcunit' , u'cppunit':u'-lcppunit' , u'c':u'', u'cpp':u''}
	cunit_version = models.CharField(max_length=16, choices=CUNIT_CHOICES,default="cunit", verbose_name=_("Unittest type or library"))


	_test_par = models.CharField(max_length = 1000, 
	    default=u"", 
	    help_text = _("Command line parameters for running TestApp"),
	    blank=True)

	#don't change next two variable names, they are fixed in checker-hierarchie
	test_description = models.TextField(help_text = _("Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded."))
	name = models.CharField(max_length=100, help_text=_("Name of the Testcase. To be displayed as title on Checker Results page"))

	_sol_name =  models.CharField(
            max_length=100,
            help_text=_("Basisfilename ( = filename without fileending!) for interaction with  MUT (Module-Under-Test)<br>" 
			+"The fileending to use gets determined by your choosen Link type.<br>"
			),
	    verbose_name=_("MUT Filename"),
	    default=u"Solution"
	)	
	_sol_ignore = models.CharField(max_length=4096, 
	    help_text=_("Regular Expression for ignoring files while compile CUT and link MUT.<br>"
		      +"CUT = Code Under Test - MUT = Module Under Test <br>"
                      +"Play with RegEx at <a href=\"http://pythex.org/\" target=\"_blank\">http://pythex.org/ </a>"
                      ),
	    default="sorry, this feature doesn't work now", blank=True, 
	    verbose_name=_("MUT ignore files")
)

        _sol_flags = models.CharField(max_length = 1000, blank = True, 
	    default=u"-Wall -Wextra -Wl,--warn-common", 
	    help_text = _("Compiler and Linker flags used while generating MUT (Module-under-Test)."),
	    verbose_name=_("MUT flags")
	)



	
	def use_cppBuilder(self):
		if 'pp' in self.cunit_version:
			return True
		else:
			return False
	
	
	def mut_flags(self,env):
		return self._sol_flags if self._sol_flags else " "
	

	def mut_output_flags(self,env):
		return self.LINK_DICT[self.link_type] +u' '+self._sol_name+u"."+self.link_type

	def test_flags(self, env):
		my_unittest_flags = self.CUNIT_DICT[self.cunit_version]
		my_flags_str = self._test_flags +u" "+my_unittest_flags
		return my_flags_str

	def test_output_flags(self,env):
		return u'-o '+self._test_name

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
	#
	# Each Instance of this CUnitChecker has a corresponding
	# c-File with main-function.
	# therefor we must hide c-main functions from other 
	# instances of this checker.
	# 
	# Now we have a look to interactin with students files:  
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
		noUnitTest_Sources = env.sources()[:] #swallow copy because env.sources() gets manipulated by time
		noUnitTest_Filenames = [ seq[0] for seq in noUnitTest_Sources ]
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
			my_flags = self.mut_flags(env) +u" " + self.test_flags(env)
			my_oflags = self.test_output_flags(env) # + self.mut_output_flags(env)

			#languageCompiler C or CPP 
			if self.use_cppBuilder():
				#CPP
				test_builder = IgnoringCXXBuilder2(_flags=my_flags ,_ignore=[], _file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags=my_oflags)
			else:
				#C
				test_builder = IgnoringCBuilder2(_flags=my_flags, _ignore=[], _file_pattern=r"^.*\.(c|C)$",_output_flags=my_oflags)
		else:
			#ignoring all test-code filenames for solution_builder
			#ignoring all non test-code filenames for test_builder
			
			import zipfile  #via src/utilities/file_operations
			
			try:
				with zipfile.ZipFile(self.file.path) as zip_file:
					names = zip_file.namelist()
			except zipfile.BadZipfile:
					import string
					import re
					cleanfilename = re.sub(r'^CheckerFiles/Task_\d*/'+self.__class__.__name__, '', self.file.name).lstrip('/')
					names = [cleanfilename]			 
			
			# shared object or executable

			my_test_flags = self.test_flags(env)
			my_mut_flags = self.mut_flags(env)
			my_test_oflags = self.test_output_flags(env)
			my_mut_oflags = self.mut_output_flags(env)

			#raise TypeError			

			#languageCompiler C or CPP 
			if self.use_cppBuilder():
				#CPP
				solution_builder = IgnoringCXXBuilder2(_flags=my_mut_flags, _ignore=names, _file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags=my_mut_oflags)
				test_builder = IgnoringCXXBuilder2(_flags=my_test_flags, _ignore=noUnitTest_Filenames, _file_pattern=r"^.*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$",_output_flags=my_test_oflags)
			else:
				#C
				solution_builder = IgnoringCBuilder2(_flags=my_mut_flags, _ignore=names, _file_pattern=r"^.*\.(c|C)$",_output_flags=my_mut_oflags)
				test_builder = IgnoringCBuilder2(_flags=my_test_flags, _ignore=noUnitTest_Filenames, _file_pattern=r"^.*\.(c|C)$",_output_flags=my_test_oflags)

			
		build_solution_result = None
		if solution_builder:
			build_solution_result = solution_builder.run(env)
			if not build_solution_result.passed:
				# result = self.create_result(env)
				# result += build_solution_result
				result.set_passed(False)
				result.set_log( '<pre>' + escape(self.test_description) + '\n\n==========  Preprocessing =============\n*    Generating "Shared Object"       *\n* or "Executable" from solution files *\n======== Failure-Results ==============\n\n</pre><br/>\n'+build_solution_result.log )
				return result

		build_test_result = test_builder.run(env) 
		if not build_test_result.passed:
			# result = self.create_result(env)
			# result += build_test_result
			result.set_passed(False)
			result.set_log( '<pre>' + escape(self.test_description) + '\n\n==========  Preprocessing =============\n*    Generating  "Testing Executable" *\n======== Failure-Results ==============\n\n</pre><br/>\n'+build_test_result.log )
			return result

		environ = {}

		environ['UPLOAD_ROOT'] = settings.UPLOAD_ROOT
                script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'scripts')

		cmd_par = self._test_par.split(' ') if self._test_par else []
		cmd = [os.path.join(script_dir,self.runner()),self._test_name] + cmd_par
		[output, error, exitcode,timed_out, oom_ed] = execute_arglist(cmd, env.tmpdir(),environment_variables=environ,timeout=settings.TEST_TIMEOUT,fileseeklimit=settings.TEST_MAXFILESIZE, extradirs=[script_dir])

		#result = self.create_result(env)

		(output,truncated) = truncated_log(output)
		output = '<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/><pre>' + escape(output) + '</pre>'


		result.set_log(output,timed_out=timed_out or oom_ed,truncated=truncated,oom_ed=oom_ed)
		result.set_passed(not exitcode and not timed_out and not oom_ed and self.output_ok(output) and not truncated)
		result.save()

		return result

class UnitCheckerCopyForm(AlwaysChangedModelForm):
		
	def __init__(self, **args):
		""" override default values for the model fields """
		super(UnitCheckerCopyForm, self).__init__(**args)
		#self.fields["_flags"].initial = ""
		#self.fields["_output_flags"].initial = ""
		#self.fields["_libs"].initial = "junit3"
		#self.fields["_file_pattern"].initial = r"^.*\.[jJ][aA][vV][aA]$"
		
		
	def clean_filename(self):
		filename = self.cleaned_data['filename']
		if (not filename.strip()):
			if 'file' in self.cleaned_data:
				file = self.cleaned_data['file']
				return (os.path.basename(file.name))
			else:
				return None
		else:			
			if 'file' in self.cleaned_data:
				file = self.cleaned_data['file']
				basename = os.path.basename(file.name)
				force = self.cleaned_data.get('force_save')
				
				if not force: 
					if not (filename == basename):
						from django import forms
						self.fields['force_save'] = forms.BooleanField(initial=True, widget=forms.HiddenInput())
						raise forms.ValidationError(_('You should check \"Filename\" value. The correct name could be: ')+basename)
					else:
						return filename
				else:
					return filename
			else:
				return filename
	

class CUnitChecker2Inline(CheckerInline):
	""" This Class defines how the the the checker is represented as inline in the task admin page. """
	model = CUnitChecker2
	verbose_name = "C/C++ Unit Checker 2"
	form = UnitCheckerCopyForm
	# graphical layout
	fieldsets = (
		(CUnitChecker2.description(), {
		'fields': ('order',
			('public', 'required', 'always', 'critical'),
			'name','test_description',
			( 'file', 'unpack_zipfile'),
			( 'path', 'filename'),
			'_sol_name',
			('_sol_ignore', '_sol_flags'),
			'_test_name',
			('_test_ignore', '_test_flags'),
			'cunit_version',
			'link_type',
			'_test_par'),
		}),
	)



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

	
