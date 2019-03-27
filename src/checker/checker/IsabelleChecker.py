# -*- coding: utf-8 -*-

from pipes import quote
import shutil, os, re, subprocess
from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker, CheckerFileField
from utilities.safeexec import execute_arglist
from utilities.file_operations import *


RXFAIL = re.compile(r"^\*\*\*", re.MULTILINE)


class IsabelleChecker(Checker):
    logic = models.CharField(max_length=100, default="HOL", help_text=_("Default heap to use"))
    additional_theories = models.CharField(max_length=200, blank=True, help_text=_("Isabelle theories to be run in addition to those provided by the user (Library theories or theories uploaded using the Create File Checker). Do not include the file extensions. Separate multiple theories by space"))

    def title(self):
        """ Returns the title for this checker category. """
        return "Isabelle-Checker"

    def output_ok(self, output):
        return (RXFAIL.search(output) == None)


    @staticmethod
    def description():
        """ Returns a description for this Checker. """
        return "Verifies that every submitted Isabelle theory can be processed without error"


    def run(self, env):

        thys = [('%s' % os.path.splitext(name__[0])[0]) for name__ in env.sources()]
        additional_thys = ['%s' % name for name in re.split(" |,", self.additional_theories) if name]
        user_thys = [name for name in thys if name not in additional_thys]

        platform = execute_arglist([settings.ISABELLE_BINARY, "getenv", "ML_PLATFORM"], env.tmpdir(), timeout=10, error_to_output=False)[0]

        args = [setting.ISABELLE_BINARY, "process"]
        # Depending on the underlying polyml platform (32/64 bit) we use 2 or 1 threads, resp.
        # This is due to the default memory limit (1gb) of safe-docker and the
        # default initial heap sizes of 500m and 1000m for 32 bit and 64 bit, resp.
        if "x86_64-linux" in platform:
            args += ["-o", "threads=1"]
        else:
            args += ["-o", "threads=2"]
        for t in additional_thys + user_thys:
            args += ["-T", t]
        args += ["-l", self.logic]

        (output, error, exitcode, timed_out, oom_ed) = execute_arglist(args, env.tmpdir(), timeout=settings.TEST_TIMEOUT, error_to_output=False)

        if timed_out:
            output += "\n\n---- check aborted after %d seconds ----\n" % settings.TEST_TIMEOUT

        if oom_ed:
            output += "\n\n---- check aborted, out of memory ----\n"

        result = self.create_result(env)
        result.set_log('<pre>' + escape(output) + '</pre>')
        result.set_passed(not timed_out and not oom_ed and self.output_ok(output))

        return result

from checker.admin import    CheckerInline

class IsabelleCheckerInline(CheckerInline):
    model = IsabelleChecker
