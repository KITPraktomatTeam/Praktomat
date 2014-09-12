# -*- coding: utf-8 -*-

from pipes import quote
import shutil, os, re, subprocess
from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.models import Checker, CheckerFileField
from utilities.safeexec import execute_arglist
from utilities.file_operations import *


class RChecker(Checker):
	r_script = models.CharField(max_length=100, help_text=_("R script to execute. If left blank, it will run any *.R file, as long as there is only one."), blank=True)


	def title(self):
		""" Returns the title for this checker category. """
		return "R-Checker"


	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		return u"Runs a submitted R script using the Rscript tool"


	def run(self, env):
		thys = map (lambda (name,_): ('"%s"' % os.path.splitext(name)[0]), env.sources())

		R_files = [
		    name
		    for (name,content) in env.sources()
		    if os.path.splitext(name)[1] == '.R'
		    ]

		scriptname = None
		if len(R_files) == 0:
			output = "<p>No R scripts found in submission</p>"
			result = self.create_result(env)
			result.set_log(output)
			result.set_passed(False)
			return result

                if self.r_script:
			if self.r_script not in R_files:
				output = "<p>Could not find expected R script %s.</p>" % self.r_script
				output += "<p>R scripts found: %s</p>" % ", ".join(map(escape, R_files))
				result = self.create_result(env)
				result.set_log(output)
				result.set_passed(False)
				return result

			scriptname = self.r_script
		else:
			if len(R_files) > 1:
				output = "<p>Multiple R scripts found in submission.</p>"
				output += "<p>R scripts found: %s</p>" % ", ".join(map(escape, R_files))
				output +=" <p>Please submit exactly one file ending in <tt>.R</tt></p>"
				result = self.create_result(env)
				result.set_log(output)
				result.set_passed(False)
				return result
			else:
				scriptname = R_files[0]

		args = ["Rscript", scriptname]
		(output, error, exitcode, timed_out) = execute_arglist(
			args,
			env.tmpdir(),
			timeout=settings.TEST_TIMEOUT,
			fileseeklimit=settings.TEST_MAXFILESIZE,
			maxmem=settings.TEST_MAXMEM,
			)

		if timed_out:
			output += "\n\n---- script execution aborted, took too long ----\n"

		if exitcode != 0:
			output += "\n\n---- Rscript finished with exitcode %d ----\n" % exitcode

		if os.path.isfile(os.path.join(env.tmpdir(), "Rplots.pdf")):
			output += "\n\n---- Note: Rplots.pdf file has been created  ----\n"

		result = self.create_result(env)
		result.set_log('<pre>' + escape(output) + '</pre>')
		result.set_passed(exitcode == 0 and not timed_out)

		return result

from checker.admin import	CheckerInline

class RCheckerInline(CheckerInline):
	model = RChecker

