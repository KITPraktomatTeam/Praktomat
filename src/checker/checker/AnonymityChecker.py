# -*- coding: utf-8 -*-

"""
AnonymityChecker.
"""

import os
import string
import re
import tempfile
import fnmatch

from django.db import models
from django.utils.translation import ugettext as _
from checker.basemodels import Checker

from django.template.defaultfilters import escape


# Helpers

def word(s):
    """Return a regular expression that matches the word S"""
    if not s:
        s =     r"\bxyzzy9332\b" # Some word that never occurs
        return s
    s = re.sub("ä|ae|&auml;",  "(ä|ae|&auml;)",  s)
    s = re.sub("ö|oe|&ouml;",  "(ö|oe|&ouml;)",  s)
    s = re.sub("ü|ue|&uuml;",  "(ü|ue|&uuml;)",  s)
    s = re.sub("ß|ss|&szlig;", "(ß|ss|&szlig;)", s)
    s = re.sub(r"\bv[oa]n\b", "", s)
    s = re.sub(" +", "", s)
    s = re.sub(r"\belse\b",     r"\bxyzzy9332\b", s)
    return r'\b' + s + r'\b'

def line(content, match):
    """Report occurrences of MATCH in CONTENT within their line"""
    start_of_line = match.start()
    while start_of_line > 0 and content[start_of_line - 1] != '\n':
        start_of_line = start_of_line - 1

    end_of_line = match.end()
    while end_of_line < len(content) and content[end_of_line] != '\n':
        end_of_line = end_of_line + 1

    line_number = 1
    i = 0
    while i < match.start():
        if content[i] == '\n':
            line_number = line_number + 1
        i = i + 1

    return (repr(line_number) + ": <tt>" +
            escape(content[start_of_line:match.start()]) +
            "<strong>" +
            escape(content[match.start():match.end()]) +
            "</strong>" +
            escape(content[match.end():end_of_line]) +
            "</tt>")


class AnonymityChecker(Checker):

    def title(self):
        """Returns the title for this checker category."""
        # _de("Anonymitaet sicherstellen")
        return _("Ensure anonymous submission")

    @staticmethod
    def description():
        """ Returns a description for this Checker. """
        #_de(u"Diese Prüfung ist bestanden, wenn alle eingereichten Dateien weder Ihren Vor- noch Ihre Nachnamen enthalten.")
        return _("This check fails if a submitted file contains your first or last name.")

    def run(self, env):
        result = self.create_result(env)
        log = ""
        passed = 1

        user = env.user()

        for (fullfname, content) in env.string_sources():
            # check anonymity

            # search for user ID or name
            regexp = re.compile((word(user.last_name)
                                 + "|" + word(user.first_name) ), re.I)

            match_iter = regexp.finditer(content)

            firstrun = 1

            while True:
                try:
                    match = next(match_iter)
                except StopIteration:
                    break

                if firstrun:
                    log += "<H4>" + escape(fullfname) + "</H4>"
                    #_de("Die Datei enth&auml;lt Ihren Namen oder Ihre Benutzerkennung:")
                    log += _("The file contains your name or user id:") + "<p>"
                    firstrun = 0
                    passed = 0

                log += line(content, match) + "<br>"


        if not passed:
            # _de("""<p>Praktomat unterstützt
            # <em>anonymes Bewerten</em> - der Bewerter kennt nur Ihr
            # Programm, nicht aber Ihren Namen.  Um anonymes Bewerten zu
            # ermöglichen, darf Ihr Name nicht im Programmtext auftreten.<p>
            # Bitte ändern Sie den Programmtext
            # und versuchen Sie es noch einmal.""")
            log += _("""<p>Praktomat supports <em>anonymous marking</em>,
i.e. the person who marks only sees your submission, but not your name or identity.
To allow anonymous marking, your name and user id is not allowed to appear in your submission.<p>
Please remove your name and user id and submit again.""")

        result.set_log(log)
        result.set_passed(passed)
        return result


from checker.admin import CheckerInline
class AnonymityCheckerInline(CheckerInline):
    model = AnonymityChecker
fieldsets = (
              (None, {
                      'fields': ("public"),
                      'description': "This is a set of fields group into a fieldset."
              }),
            )
