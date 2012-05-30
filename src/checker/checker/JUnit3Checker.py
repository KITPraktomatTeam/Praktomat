# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from checker.models import Checker, CheckerFileField, CheckerResult, execute
from checker.admin import	CheckerInline, AlwaysChangedModelForm
from utilities.file_operations import *

from checker.compiler.Builder import Builder


class JUnit3Checker(Checker):
	""" Checker for JUnit3 Unittests. Deprecated. Please use JUnitChecker """
	
	# Add fields to configure checker instances. You can use any of the Django fields. (See online documentation)
	# The fields created, task, public, required and always will be inherited from the abstract base class Checker
	name = models.CharField(max_length=100, help_text=_("The name of the Test"))
	test_case = CheckerFileField(help_text=_(u"Die JUnit3-Testfälle als Java .class File"))
	
	def title(self):
		return u"JUnit3 Checker"

	@staticmethod
	def description():
		return u"Deprecated!!! Please use the JUnitChecker"

	def requires(self):
		return [ Builder ]	

	
	def run(self, env):
		""" Do whatever this checker is suposed to do. """
		copy_file_to_directory_verbatim(self.test_case.path,env.tmpdir())
		junit_class = os.path.basename(self.test_case.path).rsplit('.',1).pop(0)

		cmd = settings.JUNIT38 + " -text " + junit_class

		[output, error, exitcode] = execute(cmd, env.tmpdir())

		result = CheckerResult(checker=self)			
		result.set_log('<pre>' + output + '</pre>')
		result.set_passed(not exitcode)
		return result


class ExampleCheckerInline(CheckerInline):
	""" This Class defines how the the the checker is represented as inline in the task admin page. """
	model = JUnit3Checker


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

	
