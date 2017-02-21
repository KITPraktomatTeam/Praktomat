# -*- coding: utf-8 -*-

"""
TextChecker.
"""

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker

class TextChecker(Checker):
    """ Checks if the specified text is included in a submitted file """

    #Code OTH Regensburg Francesco Cucinotta
    SET_OF_CHOICES = [(0,'The text must not be in the solution'),
                      (1,'The text has to be in the solution'),]

    text = models.TextField()
    choices = models.IntegerField(default=1, verbose_name='Select:', choices=SET_OF_CHOICES,blank=False)


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
        gotoFind = ""

        # search the sources
        for (name, content) in env.sources():
            lines = self._getLines(content)
            lineNum = 1
            for line in lines:
                if line.find(self.text) >= 0:
                    gotoFind = 1

                if not inComment:
                    if line.find('/*') >= 0:
                        parts = line.split('/*')
                        if parts[0].find(self.text) >= 0:
                             occurances.append((name, lineNum))
                        inComment = False

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

                if line.find(self.text) >= 0:
                        gotoFind = 1

                lineNum += 1


        # Print Results:
        if  gotoFind == 1:
            if self.choices == 1:
                if len(occurances) <= 0:
                    passed = 0
                    log = "<strong>" + "'" + escape(self.text) + "'" + "</strong>" + u" kommt nicht in Ihrer Lösung vor!"
                else:
                    log = "<strong>" + "'" + escape(self.text) + "'" + "</strong>" + " kommt an folgenden Stellen vor<br>"
                    for (name, num) in occurances:
                        log += escape(name) + " Zeile: " + str(num) + "<br>"
            else:
                log = "<strong>" + "'" + escape(self.text) + "'" + "</strong>" + " kommt an folgenden Stellen vor<br>"
                for (name, num) in occurances:
                    log += escape(name) + " Zeile: " + str(num) + "<br>"
                passed = 0
        else:
            if self.choices == 1:
                log = "<strong>" + "'" + escape(self.text) + "'" + "</strong>" + u" kommt nicht in Ihrer Lösung vor!"
                passed = 0
            elif self.choices == 0:
                log = "<strong>"+"'"+escape(self.text)+"'"+"</strong>" + u" kommt nicht in Ihrer Lösung vor!"


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
