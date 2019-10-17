# -*- coding: utf-8 -*-

import shutil, os, re, subprocess
from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker, CheckerFileField
from utilities.safeexec import execute_arglist
from utilities.file_operations import *

class CheckStyleChecker(Checker):

    name = models.CharField(max_length=100, default="CheckStyle", help_text=_("Name to be displayed on the solution detail page."))
    configuration = CheckerFileField(help_text=_("XML configuration of CheckStyle. See http://checkstyle.sourceforge.net/"))

    def title(self):
        """ Returns the title for this checker category. """
        return self.name

    @staticmethod
    def description():
        """ Returns a description for this Checker. """
        return "Runs checkstyle (http://checkstyle.sourceforge.net/)."


    def run(self, env):

        # Save save check configuration
        config_path = os.path.join(env.tmpdir(), "checks.xml")
        copy_file(self.configuration.path, config_path)

        # Run the tests
        args = [settings.JVM, "-cp", settings.CHECKSTYLEALLJAR, "-Dbasedir=.", "com.puppycrawl.tools.checkstyle.Main", "-c", "checks.xml"] + [name for (name, content) in env.sources()]
        [output, error, exitcode, timed_out, oom_ed] = execute_arglist(args, env.tmpdir())

        # Remove Praktomat-Path-Prefixes from result:
        output = re.sub(r"^"+re.escape(env.tmpdir())+"/+", "", output, flags=re.MULTILINE)

        result = self.create_result(env)

        log = '<pre>' + escape(output) + '</pre>'
        if timed_out:
            log = log + '<div class="error">Timeout occured!</div>'
        if oom_ed:
            log = log + '<div class="error">Out of memory!</div>'
        result.set_log(log)


        result.set_passed(not timed_out and not oom_ed and not exitcode and (not re.match('Starting audit...\nAudit done.', output) == None))

        return result

from checker.admin import    CheckerInline

class CheckStyleCheckerInline(CheckerInline):
    model = CheckStyleChecker
