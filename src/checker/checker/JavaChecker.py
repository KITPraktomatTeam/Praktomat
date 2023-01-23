# -*- coding: utf-8 -*-

from django.db import models
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from . JUnitChecker import RXFAIL
from checker.admin import CheckerInline
from checker.basemodels import Checker, truncated_log
from utilities.file_operations import *
from utilities.safeexec import execute_arglist


class JavaChecker(Checker):
    def title(self):
        return "Java Checker"

    # Add fields to configure checker instances. You can use any of the Django fields. (See online documentation)
    # The fields created, task, public, required and always will be inherited from the abstract base class Checker
    class_name = models.CharField(
        max_length=100,
        help_text=_("The fully qualified name of the test case class (without .class)")
    )
    test_description = models.TextField(
        help_text=_("Description of the Testcase. To be displayed on Checker Results page when checker is unfolded."))
    name = models.CharField(max_length=100,
        help_text=_("Name of the Testcase. To be displayed as title on Checker Results page"))

    def title(self):
        return u"Java based test: " + self.name

    @staticmethod
    def description():
        return u"This Checker runs a java class. The java class must be existing in the sandbox, or in the folder '" \
               + settings.JAVA_CUSTOM_LIBS + \
               u"'. You may want to use CreateFile Checker to " \
               u"upload the .jar or java file and possibly input data files in the " \
               u"sandbox before running this check. " \
               u"JUnit tests will only be able to read input data files if they are " \
               u"placed in the data/ subdirectory. The following arguments will be " \
               u"passed to the main routine in the specified class: sandbox directory, " \
               u"user id, mat_number, solution id"

    def output_ok(self, output):
        return RXFAIL.search(output) is None

    def run(self, env):
        environ = {'UPLOAD_ROOT': settings.UPLOAD_ROOT, 'JAVA': settings.JVM}

        script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')
        environ['POLICY'] = os.path.join(script_dir, "junit.policy")
        cmd = [settings.JVM_SECURE, "-cp", settings.JAVA_CUSTOM_LIBS + ":*", self.class_name, 
            env.tmpdir(),
            str(env.user().id),
            str(env.user().mat_number),
            str(env.user().first_name),
            str(env.user().last_name),
            str(env.solution().id),
            str(env.user().username)]
        [output, error, exitcode, timed_out, oom_ed] = execute_arglist(cmd, env.tmpdir(), environment_variables=environ,
            timeout=settings.TEST_TIMEOUT, fileseeklimit=settings.TEST_MAXFILESIZE, filenumberlimit=settings.TEST_MAXFILENUMBER, extradirs=[script_dir])

        result = self.create_result(env)

        (output, truncated) = truncated_log(output)
        output = '<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/><pre>' + \
                 escape(output) + '</pre>'
        result.set_log(output, timed_out=timed_out or oom_ed, truncated=truncated, oom_ed=oom_ed)
        result.set_passed(not exitcode and not timed_out and not oom_ed and self.output_ok(output) and not truncated)
        return result


class JavaCheckerInline(CheckerInline):
    """ This Class defines how the the the checker is represented as inline in the task admin page. """
    model = JavaChecker
