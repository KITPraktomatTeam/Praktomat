# -*- coding: utf-8 -*-
from __future__ import unicode_literals


"""
InterfaceChecker.
"""

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker

class InterfaceChecker(Checker):

    ## use interface model class instead as soon as nested admin inlines are possible (see below)
    interface1 = models.CharField(max_length=100, help_text=_("The name of the interface that must be implemented."))
    interface2 = models.CharField(max_length=100, blank = True, help_text=_("The name of the interface that must be implemented."))
    interface3 = models.CharField(max_length=100, blank = True, help_text=_("The name of the interface that must be implemented."))
    interface4 = models.CharField(max_length=100, blank = True, help_text=_("The name of the interface that must be implemented."))
    interface5 = models.CharField(max_length=100, blank = True, help_text=_("The name of the interface that must be implemented."))
    interface6 = models.CharField(max_length=100, blank = True, help_text=_("The name of the interface that must be implemented."))
    interface7 = models.CharField(max_length=100, blank = True, help_text=_("The name of the interface that must be implemented."))

    def title(self):
        """ Returns the title for this checker category. """
        return "Interface Checker"

    @staticmethod
    def description():
        """ Returns a description for this Checker. """
        s = "Diese Prüfung ist bestanden, wenn alle vorgegebenen Interfaces implementiert wurden."
        return s

    def run(self, env):
        """  Test if all interfaces were implemented correctly
        If so, the interfaces are added to make it possible to compile them  """
        result = self.create_result(env)

        implemented = []
        passed = 1
        log = ""

        # Define regular expressions for interfaces implemented by a class
        # baseExp for classes implementing only one interface, extExp for more
        baseExp = "^ *((public )|(protected )|(private ))?class +[A-Z][0-9a-zA-Z_]* *implements +"
        extExp = baseExp + "[0-9a-zA-Z_, ]*"

        # Iterate through sources and find out which interfaces were implemented
        for (name, content) in env.string_sources():
            for interface in [self.interface1, self.interface2, self.interface3, self.interface4, self.interface5, self.interface6, self.interface7]: ##self.interface_set.all()

                iname = interface ##.name
                noComments = self._cutComments(content) # remove comments

                expression = re.compile(baseExp + self._cleanName(iname), re.MULTILINE)
                if expression.search(noComments):
                    if not iname in implemented:
                        implemented.append(iname)

                expression = re.compile(extExp + self._cleanName(iname), re.MULTILINE)
                if expression.search(noComments):
                    if not iname in implemented:
                        implemented.append(iname)

        # check if all interfaces were implemented
        for interface in [self.interface1, self.interface2, self.interface3, self.interface4, self.interface5, self.interface6, self.interface7]: ##self.interface_set.all()
            if not interface in implemented: ## interface.name
                passed = 0
                log += "Interface " + escape(interface) + " wurde nicht implementiert.<BR>" ## interface.name

        if not passed:
            log += """<p>Sie müssen alle vorgegebenen Interfaces implementieren.
                      Bitte ändern Sie Ihr Programm so ab, dass es den
                      Anforderungen entspricht und versuchen Sie es erneut.</p> """

        result.set_log(log)
        result.set_passed(passed)
        return result

    def _cutComments(self, content):
        """ Removes all java comments of the form /* ... */ or /** ... */
        This prevents cheating """
        noComments = ""

        #split the strings
        partstmp = content.split('/*')
        parts = []
        for string in partstmp:
            parts.extend(string.split('*/'))

        # the 1st (index 0), 3rd(index 2), 5th etc. parts are not comments
        # so we will save only those in our string
        i = 0
        while i < len(parts):
            noComments += parts[i]
            i+=2

        return noComments

    def _cleanName(self, name):
        """ Extracts the name of the interface/class from the filename, e.g.
        _cleanName(INet.java) returns INet """
        return name.split('.').pop(0)


## No nested inlines in Django 1.0.2 admin -> fixed amount of interfacenames into interface checker
##class Interface(models.Model):
##    checker = models.ForeignKey(InterfaceChecker)
##    name = models.CharField(max_length=100, help_text=_("The name of the interface that must be implemeted."))
##
##    class Meta:
##        # Required for syncdb as of django 1.0.2 - the same as in Checker class!
##        app_label = 'checker'




##from django.contrib import admin
##class InterfaceInline(admin.TabularInline):
##    model = Interface
##    extra = 6


from checker.admin import    CheckerInline

class InterfaceCheckerInline(CheckerInline):
    model = InterfaceChecker
##    inlines =  [InterfaceInline]
