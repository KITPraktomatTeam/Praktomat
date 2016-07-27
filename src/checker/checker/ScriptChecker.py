# -*- coding: utf-8 -*-

import os, re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from django.utils.encoding import force_unicode
from checker.basemodels import Checker, CheckerFileField, truncated_log
from utilities.safeexec import execute_arglist
from utilities.file_operations import *

class ScriptChecker(Checker):

	name = models.CharField(max_length=100, default="Externen Tutor ausführen", help_text=_("Name to be displayed on the solution detail page."))
	shell_script = CheckerFileField(help_text=_("A script (e.g. a shell script) to run. Its output will be displayed to the user (if public), the checker will succeed if it returns an exit code of 0. The environment will contain the variables JAVA and PROGRAM."))
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
		copy_file(self.shell_script.path, env.tmpdir(), to_is_directory=True)
		os.chmod(env.tmpdir()+'/'+os.path.basename(self.shell_script.name),0750)
		
		# Run the tests -- execute dumped shell script 'script.sh'

		filenames = [name for (name,content) in env.sources()]
		args = [env.tmpdir()+'/'+os.path.basename(self.shell_script.name)] + filenames

		environ = {}
		environ['USER'] = str(env.user().id)
		environ['HOME'] = env.tmpdir()
		environ['JAVA'] = settings.JVM
		environ['JAVA_SECURE'] = settings.JVM_SECURE
		environ['POLICY'] = settings.JVM_POLICY
		environ['PROGRAM'] = env.program() or ''

		script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'scripts')
		

		[output, error, exitcode,timed_out, oom_ed] = execute_arglist(
                            args,
                            working_directory=env.tmpdir(),
                            environment_variables=environ,
                            timeout=settings.TEST_TIMEOUT,
                            maxmem=settings.TEST_MAXMEM,
                            fileseeklimit=settings.TEST_MAXFILESIZE,
                            extradirs = [script_dir],
                            )
		output = force_unicode(output, errors='replace')

		result = self.create_result(env)
		(output,truncated) = truncated_log(output)

		if self.remove:
			output = re.sub(self.remove, "", output)
		if not self.returns_html or truncated or timed_out or oom_ed:
			output = '<pre>' + escape(output) + '</pre>'

		result.set_log(output,timed_out=timed_out,truncated=truncated,oom_ed=oom_ed)
		result.set_passed(not exitcode and not timed_out and not oom_ed and not truncated)
		
		return result
	
from checker.admin import	CheckerInline
from django import forms
from django.contrib import messages
from django.contrib import admin

class WarningScriptCheckerFormSet(forms.BaseInlineFormSet):
	class Meta:
		model = ScriptChecker
		exclude = []

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(WarningScriptCheckerFormSet, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		scriptcheckers = super(WarningScriptCheckerFormSet, self).save(*args, **kwargs)

		for checker in scriptcheckers:
			script = checker.shell_script
			# Workaround that may not be necerssay anymore  in Django > 1.8,
			# see https://code.djangoproject.com/ticket/13809 and https://code.djangoproject.com/ticket/26398
			script.close()
			script.file.close()

			# In Universal Newline mode, python will collect encountered newlines
			script.open(mode="rU")
			# make sure self.newlines is populated
			script.readline()
			script.readline()
			script.readline()

			if (script.newlines is None) or ("\r\n" in script.newlines):
				messages.add_message(self.request, messages.WARNING, "Script File %s does not appear to use UNIX line-endings. Instead it uses: %s" % (script.name, repr(script.newlines)))

			script.close()
		
		return scriptcheckers

class ScriptCheckerInline(CheckerInline):
	model = ScriptChecker

	formset = WarningScriptCheckerFormSet
	def get_formset(self, request, obj=None, **kwargs):
		AdminFormset = super(ScriptCheckerInline, self).get_formset(request, obj, **kwargs)

		class AdminFormsetWithRequest(AdminFormset):
			def __new__(cls, *args, **kwargs):
				kwargs['request'] = request
				return AdminFormset(*args, **kwargs)

		return AdminFormsetWithRequest

