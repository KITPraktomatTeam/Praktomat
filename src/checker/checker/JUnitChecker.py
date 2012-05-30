# -*- coding: utf-8 -*-

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.models import Checker, CheckerFileField, CheckerResult, execute
from checker.admin import	CheckerInline, AlwaysChangedModelForm
from utilities.file_operations import *

from checker.compiler.JavaBuilder import JavaBuilder

RXFAIL	   = re.compile(r"^(.*)(FAILURES!!!|your program crashed|cpu time limit exceeded|ABBRUCH DURCH ZEITUEBERSCHREITUNG)(.*)$",	re.MULTILINE)

class JUnitChecker(Checker):
	""" New Checker for JUnit3 Unittests. """
	
	# Add fields to configure checker instances. You can use any of the Django fields. (See online documentation)
	# The fields created, task, public, required and always will be inherited from the abstract base class Checker
	class_name = models.CharField(max_length=100, help_text=_("The fully qualified name of the Testcase class"))
	# description = models.CharField(max_length=5000, help_text=_("Description of the Testcase"))
	test_description = models.TextField(help_text = _("Description of the Testcase."))
	
	def title(self):
		return u"JUnit Tests"

	@staticmethod
	def description():
		return u"This Checker runs a JUnit 3 Testcases existing in the sandbox. You may want to use CreateFile Checker to create JUnit .java files in the sandbox before running the JavaBuilder."

	def output_ok(self, output):
		return (RXFAIL.search(output) == None)

	def run(self, env):
		java_builder = JavaBuilder(_flags="", _libs="junit3",_file_pattern=r"^.*\.[jJ][aA][vV][aA]$",_output_flags="")

		build_result = java_builder.run(env)

		if not build_result.passed:
			result = CheckerResult(checker=self)
			result.set_passed(False)
			result.set_log('<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/>\n'+build_result.log)
			return result

		environ = {}

		environ['UPLOAD_ROOT'] = settings.UPLOAD_ROOT
		environ['JAVA'] = settings.JVM
		environ['POLICY'] = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),"scripts"),"junit.policy")
		environ['USE_KILL_LOG'] = "False" 
		environ['ULIMIT_FILESIZE'] = '128'  # Have the checker script set a filesize-ulimit of 128kb
		                                    # Specifically, this limits the DejaGNU .log file size,
		                                    # and thus deals with Programs that output lots of junk

		cmd = settings.JVM_SECURE  + " -cp " + settings.JUNIT38_JAR + ":." + " junit.textui.TestRunner " + self.class_name
		[output, error, exitcode] = execute(cmd, env.tmpdir(),environment_variables=environ)

		result = CheckerResult(checker=self)
		
		result.set_log('<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/><pre>' + escape(output) + '</pre>')
		result.set_passed((not exitcode) and self.output_ok(output))
		return result

#class JUnitCheckerForm(AlwaysChangedModelForm):
#	def __init__(self, **args):
#		""" override default values for the model fields """
#		super(JUnitCheckerForm, self).__init__(**args)
#		self.fields["_flags"].initial = ""
#		self.fields["_output_flags"].initial = ""
#		self.fields["_libs"].initial = "junit3"
#		self.fields["_file_pattern"].initial = r"^.*\.[jJ][aA][vV][aA]$"
	
class JavaBuilderInline(CheckerInline):
	""" This Class defines how the the the checker is represented as inline in the task admin page. """
	model = JUnitChecker
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

	
