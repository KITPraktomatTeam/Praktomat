# -*- coding: utf-8 -*-

from pipes import quote
import shutil, os, re, subprocess
from django.conf import settings 

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.models import Checker, CheckerResult, CheckerFileField, execute
from utilities.file_operations import *

class CheckStyleChecker(Checker):

	name = models.CharField(max_length=100, default="CheckStyle", help_text=_("Name to be displayed on the solution detail page."))
	configuration = CheckerFileField(help_text=_("XML configuration of CheckStyle. See http://checkstyle.sourceforge.net/"))
	
	def title(self):
		""" Returns the title for this checker category. """
		return self.name
	
	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		return u"Runs checkstyle (http://checkstyle.sourceforge.net/)."
	

	def run(self, env):

		# Save save check configuration
		config_path = os.path.join(env.tmpdir(), "checks.xml")
		copy_file(self.configuration.path, config_path)
		
		# Run the tests
		args = [settings.JVM, "-cp", settings.CHECKSTYLEALLJAR, "-Dbasedir=.", "com.puppycrawl.tools.checkstyle.Main", "-c", "checks.xml"] + [quote(name) for (name,content) in env.sources()]
		(output, error, exitcode) = execute(args, env.tmpdir())
		
		# Remove Praktomat-Path-Prefixes from result:
		output = re.sub(r"^"+re.escape(env.tmpdir())+"/+","",output,flags=re.MULTILINE)

		result = CheckerResult(checker=self)
		result.set_log('<pre>' + escape(output) + '</pre>')
		
		result.set_passed(not error and not re.match('Starting audit...\nAudit done.', output) == None)
		
		return result
	
from checker.admin import	CheckerInline

class CheckStyleCheckerInline(CheckerInline):
	model = CheckStyleChecker

