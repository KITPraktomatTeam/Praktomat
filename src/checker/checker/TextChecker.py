# -*- coding: utf-8 -*-

"""
TextChecker.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker

class TextChecker(Checker):
	""" Checks if the specified text is included in a submitted file """

	text = models.TextField(help_text=_("The text that has to be in the solution."))
	
	def title(self):
		"""Returns the title for this checker category."""
		return "Text Checker"
	
	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		return u"Diese Prüfung ist bestanden, wenn der eingegebene Text in einer Lösung gefunden wird."
		
	
	def run(self, env):
		""" Checks if the specified text is included in a submitted file """
		result = self.create_result(env)
		
		lines = []
		occurances = []
		passed = 1
		log = ""
		lineNum = 1
		inComment = False
		
		# search the sources			   
		for (name, content) in env.sources():
			lines = self._getLines(content)
			lineNum = 1
			for line in lines:
				if not inComment:
					if line.find('/*') >= 0:
						parts = line.split('/*')
						if parts[0].find(self.text) >= 0:
							occurances.append((name, lineNum))
						inComment = True	 
				 
				if not inComment:		 
						parts = line.split('//')
						if parts[0].find(self.text) >= 0:
							occurances.append((name, lineNum))				 
				else:
					if line.find('*/') >= 0:
						parts = line.split('*/')
						if len(parts) > 1:
							if parts[1].find(self.text) >= 0:
								occurances.append((name, lineNum))
							
						inComment = False
				
				lineNum += 1
		
		# Print Results:
		if len(occurances) <= 0:
			passed = 0
			log = escape(self.text) + u" kommt nicht in Ihrer Lösung vor!"
		else:
			log = escape(self.text) + " kommt an folgenden Stellen vor<br>"
			for (name, num) in occurances:
				log	 += escape(name) + " Zeile: " + str(num) + "<br>" 
		
		result.set_log(log)
		result.set_passed(passed)
		
		return result
		
	def _getLines(self, text):
		""" Returns a list of lines (as strings) from text """
		lines = text.split("\n")
		return lines

from checker.admin import	CheckerInline

class TextCheckerInline(CheckerInline):
	model = TextChecker
