# -*- coding: utf-8 -*-

import shutil, os, re, subprocess
from django.conf import settings 

from django.db import models
from django.utils.translation import ugettext_lazy as _
from praktomat.checker.models import Checker, CheckerResult

class CheckStyleChecker(Checker):

	name = models.CharField(max_length=100, default="CheckStyle", help_text=_("Name to be displayed on the solution detail page."))
	configuration = models.TextField(help_text=_("XML configuration of CheckStyle. See http://checkstyle.sourceforge.net/"))
	
	def title(self):
		""" Returns the title for this checker category. """
		return self.name
	
	def description(self):
		""" Returns a description for this Checker. """
		return u"Runs checkstyle (http://checkstyle.sourceforge.net/)."
	

	def run(self, env):

		# Save save check configuration
		config_path = os.path.join(env.tmpdir(), "checks.xml")
		config_file = open(config_path, 'w')
		config_file.write(self.configuration)
		config_file.close()
		
		# Run the tests -- execute dumped shell script 'script.sh'
		args = [settings.JVM, "-cp", settings.CHECKSTYLEALLJAR, "-Dbasedir=.", "com.puppycrawl.tools.checkstyle.Main", "-c", "checks.xml"] + [name for (name,content) in env.sources()]
		environ = os.environ 
		# needs timeout!
		
		(output, error) = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=env.tmpdir(), env=environ).communicate()
		
		result = CheckerResult(checker=self)
		result.set_log('<pre>' + output + '</pre>')
		
		result.set_passed(not error and not re.match('Starting audit...\nAudit done.', output) == None)
		
		return result
	
from praktomat.checker.admin import	CheckerInline

class CheckStyleCheckerInline(CheckerInline):
	model = CheckStyleChecker

