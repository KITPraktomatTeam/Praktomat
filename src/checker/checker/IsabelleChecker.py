# -*- coding: utf-8 -*-

from pipes import quote
import shutil, os, re, subprocess
from django.conf import settings 

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.models import Checker, CheckerResult, CheckerFileField, execute, execute_arglist
from utilities.file_operations import *

class IsabelleChecker(Checker):
	logic = models.CharField(max_length=100, default="HOL", help_text=_("Default heap to use"))

	def title(self):
		""" Returns the title for this checker category. """
		return "Isabelle-Checker"
	
	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		return u"Verifies that every submitted Isabelle theory can be processed without error"
	

	def run(self, env):

		# Find out the path to isabaelle-process
		args = [settings.ISABELLE_BINARY, "getenv", "-b", "ISABELLE_PROCESS"]
		(output, error, exitcode) = execute(args, env.tmpdir())

		isabelle_process = output.rstrip()

		total_output = ""
		for (name,content) in env.sources():
			args = [isabelle_process, "-S", "-r", "-I",  self.logic]
			(output, error, exitcode) = execute_arglist(args, env.tmpdir(), stdin_file=os.path.join(env.tmpdir(),name))

			# Remove Praktomat-Path-Prefixes from result:
			# output = re.sub(r"^"+re.escape(env.tmpdir())+"/+","",output,flags=re.MULTILINE)
			total_output += output

		result = CheckerResult(checker=self)			
		result.set_log('<pre>' + escape(total_output) + '</pre>')
		result.set_passed(True)
		
		return result
	
from checker.admin import	CheckerInline

class IsabelleCheckerInline(CheckerInline):
	model = IsabelleChecker

