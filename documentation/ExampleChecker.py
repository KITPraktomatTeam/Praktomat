# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from checker.models import Checker, CheckerResult, execute
from checker.admin import	CheckerInline, AlwaysChangedModelForm
from utilities.file_operations import *


class ExampleChecker(Checker):
	""" This class is an minimalistic example on how to implement a new checker. """

	# Add fields to configure checker instances. You can use any of the Django fields. (See online documentation)
	# The fields created, task, public, required and always will be inherited from the abstract base class Checker
	configuration_field = models.CharField(max_length=100, blank=True, default="I'm a test.", help_text=_("This text will be displayed under Charfield in the admin."))

	def title(self):
		""" Return the name of this instance of the checker. This will be shown to the user if the checker is public. """
		return "Example Checker"

	@classmethod
	def description():
		""" Returns a description for this Checker which will be displayed in the admin interface. """
		return "This class is an minimalistic example on how to implement a new checker."

	#def requires(self):
		#""" Returns the list of passed Checkers required by this checker. If the returned checker have not been passed this checker will fail automatically """
		#from checker.compiler.Builder import Builder
		#return [ Builder ]


	def run(self, env):
		""" Do whatever this checker is supposed to do. """

		# use env.tmpdir() to get the sandbox folder
		# env.sources() contains the uploaded files ala [(unicode_name, unicode_content)...] - all these files will exist in the sandbox folder
		# env.user() returns the author of the solution

		# to pass information to a checker which runs at a later time save it in env, but make sure the checkers will be executed in the right order.

		# if you need to to create or copy files use the methods from utilities.file_operations - these will alter the owner and rights of the files appropriately
		# if you need to run external programs/scripts use execute(...) - this will ensure that it will be executed with a user with restricted rights - if so configured

		# Create a result
		result = CheckerResult(checker=self)
		# Set the massage for the user and if this checker has passed then return it.
		result.set_log(self.configuration_field)
		result.set_passed(True)
		return result


class ExampleCheckerInline(CheckerInline):
	""" This Class defines how the the the checker is represented as inline in the task admin page. """
	model = ExampleChecker


# A more advanced example: By overwriting the form of the checkerinline the initial values of the inherited attributes can be overwritten.
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

