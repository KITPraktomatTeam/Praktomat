# -*- coding: utf-8 -*-

"""
Line width checker
"""

import string

from django.db import models
from django.utils.translation import ugettext_lazy as _
from praktomat.checker.models import Checker, CheckerResult

class LineWidthChecker(Checker):

	max_line_length = models.IntegerField(default = 80, help_text=_("The maximum lenght of a line of code."))

	def title(self):
		""" Returns the title for this checker category. """
		return "Maximale Zeilenbreite"
	
	def description(self):
		""" Returns a description for this Checker. """
		s = u"""Diese Prüfung ist bestanden,
			wenn keine Zeile des Programmtext breiter als
			%d Zeichen ist.""" % self.max_line_length
		return s
	
	def setup_line(self, line, env):
		""" This is a helper procedure.	 Expand tabs and likewise. """
		line = string.replace(line, "\r", "")
		line = string.expandtabs(line, env.tab_width())
		return line
		
	def run(self, env):
		""" Here's the actual work.	 This runs the check in the environment ENV,
		returning a CheckerResult. """
		result = CheckerResult(checker=self)

		log = ""
		passed = 1

		# Here's how to access the sources.
		for (name, content) in env.sources():
			if not name or not content:
				continue

			max_line_length = 0
			line_number = 1
			for line in string.split(content, "\n"):
				line = self.setup_line(line, env)
				
				if len(line) > self.max_line_length:
					msg = ( name + ":" + `line_number` +
						   ": Zeile zu breit (" + `len(line)` + " Zeichen)" + "<BR>")
					log = log + msg
					passed = 0

				max_line_length = max(len(line), max_line_length)

				line_number = line_number + 1

			msg = (name + ": Maximale Zeilenbreite: " +
				   `max_line_length` + " Zeichen\n" + "<BR>")
			log = log + msg

		# At the end of each run, be sure to set LOG and PASSED.
		result.set_log(log)
		result.set_passed(passed)

		# That's all!
		return result

from praktomat.checker.admin import CheckerInline
class LineWidthCheckerInline(CheckerInline):
	model = LineWidthChecker
