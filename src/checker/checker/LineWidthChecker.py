# -*- coding: utf-8 -*-

"""
Line width checker
"""

import string
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker

class LineWidthChecker(Checker):

	max_line_length = models.IntegerField(default = 80, help_text=_("The maximum length of a line of code."))
	tab_width =  models.IntegerField(default = 4, help_text=_("The amount of characters a tab represents."))
	include = models.CharField(max_length=100, blank = True, default=".*", help_text=_("Regular expression describing the filenames to be checked. Case Insensetive. Blank: use all files."))
	exclude = models.CharField(max_length=100, blank = True, default=".*\.txt$", help_text=_("Regular expression describing included filenames, which shall be excluded. Case Insensetive. Blank: use all files."))
	
	def title(self):
		""" Returns the title for this checker category. """
		return "Maximale Zeilenbreite (%d Zeichen)" % self.max_line_length

	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		s = u"Diese Prüfung ist bestanden, wenn keine Zeile des Programmtext breiter als die angegebene Anyahl Zeichen ist."
		return s
	
	def setup_line(self, line, env):
		""" This is a helper procedure.	 Expand tabs and likewise. """
		line = string.replace(line, "\r", "")
		line = string.expandtabs(line, self.tab_width)
		return line
		
	def run(self, env):
		""" Here's the actual work.	 This runs the check in the environment ENV,
		returning a CheckerResult. """
		result = self.create_result(env)

		log = ""
		passed = 1

		include_re = re.compile(self.include, re.IGNORECASE)
		exclude_re = re.compile(self.exclude, re.IGNORECASE)
		
		sources = env.sources()
		if self.include: sources = filter(lambda (name, content): include_re.search(name), sources)
		if self.exclude: sources = filter(lambda (name, content): not exclude_re.search(name), sources)
		
		for (name, content) in sources:
			if not name or not content:
				continue

			max_line_length = 0
			line_number = 1
			for line in string.split(content, "\n"):
				line = self.setup_line(line, env)
				
				if len(line) > self.max_line_length:
					msg = ( escape(name) + ":" + `line_number` +
						   ": Zeile zu breit (" + `len(line)` + " Zeichen)" + "<BR>")
					log = log + msg
					passed = 0

				max_line_length = max(len(line), max_line_length)

				line_number = line_number + 1

			msg = (escape(name) + ": Maximale Zeilenbreite: " +
				   `max_line_length` + " Zeichen\n" + "<BR>")
			log = log + msg

		# At the end of each run, be sure to set LOG and PASSED.
		result.set_log(log)
		result.set_passed(passed)

		# That's all!
		return result

from checker.admin import CheckerInline
class LineWidthCheckerInline(CheckerInline):
	model = LineWidthChecker
