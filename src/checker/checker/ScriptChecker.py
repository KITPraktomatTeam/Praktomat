# -*- coding: utf-8 -*-

import os, re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from checker.models import Checker, CheckerFileField, CheckerResult, execute
from utilities.file_operations import *

class ScriptChecker(Checker):

	name = models.CharField(max_length=100, default="Externen Tutor ausführen", help_text=_("Name to be displayed on the solution detail page."))
	shell_script = CheckerFileField(help_text=_("The shell script whose output for the given input file is compared to the given output file."))
	remove = models.CharField(max_length=5000, blank=True, help_text=_("Regular expression describing passages to be removed from the output."))
	returns_html = models.BooleanField(default= False, help_text=_("If the script doesn't return HTML it will be enclosed in &lt; pre &gt; tags."))

	
	def title(self):
		""" Returns the title for this checker category. """
		return self.name
	
	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		return u"Diese Prüfung wird bestanden, wenn das externe Programm keinen Fehlercode liefert."
	

	def run(self, env):
		""" Runs tests in a special environment. Here's the actual work. 
		This runs the check in the environment ENV, returning a CheckerResult. """

		# Setup
		test_dir	 = env.tmpdir()
		replace = [(u'PROGRAM',env.program())] if env.program() else []
		copy_file_to_directory(self.shell_script.path, test_dir, replace=replace)
		
		# Run the tests -- execute dumped shell script 'script.sh'
		args = ["sh",  os.path.basename(self.shell_script.name)]
		environ = {}
		environ['USER'] = env.user().get_full_name()
		environ['HOME'] = test_dir
		
		(output, error, exitcode) = execute(args, working_directory=test_dir, environment_variables=environ)

		result = CheckerResult(checker=self)
		if self.remove:
			output = re.sub(self.remove, "", output)
		if not self.returns_html:
			output = '<pre>' + output + '</pre>'
		result.set_log(output)
		result.set_passed(not error)
		
		return result
	
from checker.admin import	CheckerInline

class ScriptCheckerInline(CheckerInline):
	model = ScriptChecker

