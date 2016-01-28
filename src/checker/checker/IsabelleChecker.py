# -*- coding: utf-8 -*-

from pipes import quote
import shutil, os, re, subprocess
from django.conf import settings 

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.models import Checker, CheckerResult, CheckerFileField, execute, execute_arglist
from utilities.file_operations import *


RXFAIL	   = re.compile(r"^\*\*\*",	re.MULTILINE)


class IsabelleChecker(Checker):
	logic = models.CharField(max_length=100, default="HOL", help_text=_("Default heap to use"))

	def title(self):
		""" Returns the title for this checker category. """
		return "Isabelle-Checker"

	def output_ok(self, output):
		return (RXFAIL.search(output) == None)

	
	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		return u"Verifies that every submitted Isabelle theory can be processed without error"
	

	def run(self, env):

		# Find out the path to isabaelle-process
		args = [settings.ISABELLE_BINARY, "getenv", "-b", "ISABELLE_PROCESS"]
		(output, error, exitcode, _) = execute_arglist(args, env.tmpdir())

		isabelle_process = output.rstrip()

		thys = map (lambda (name,_): ('"%s"' % os.path.splitext(name)[0]), env.sources())

		ml_cmd = 'Secure.set_secure (); use_thys [%s]' % ','.join(thys)
		args = [isabelle_process, "-r", "-q", "-e",  ml_cmd, self.logic]
		(output, error, exitcode, timed_out) = execute_arglist(args, env.tmpdir(),timeout=settings.TEST_TIMEOUT)

		if timed_out:
			output += "\n\n---- check aborted after %d seconds ----\n" % settings.TEST_TIMEOUT

		result = CheckerResult(checker=self)			
		result.set_log('<pre>' + escape(output) + '</pre>')
		result.set_passed(not timed_out and self.output_ok(output))
		
		return result
	
from checker.admin import	CheckerInline

class IsabelleCheckerInline(CheckerInline):
	model = IsabelleChecker

