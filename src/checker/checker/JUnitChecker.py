# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker, CheckerResult, CheckerFileField, truncated_log
from checker.admin import    CheckerInline, AlwaysChangedModelForm
from utilities.safeexec import execute_arglist
from utilities.file_operations import *
from solutions.models import Solution

from checker.compiler.JavaBuilder import JavaBuilder

RXFAIL       = re.compile(r"^(.*)(FAILURES!!!|your program crashed|cpu time limit exceeded|ABBRUCH DURCH ZEITUEBERSCHREITUNG|Could not find class|Killed|failures)(.*)$",    re.MULTILINE)

class IgnoringJavaBuilder(JavaBuilder):
    _ignore = []

    def get_file_names(self, env):
        rxarg = re.compile(self.rxarg())
        return [name for (name, content) in env.sources() if rxarg.match(name) and (not name in self._ignore)]

    # Since this checkers instances  will not be saved(), we don't save their results, either
    def create_result(self, env):
        assert isinstance(env.solution(), Solution)
        return CheckerResult(checker=self, solution=env.solution())

class JUnitChecker(Checker):
    """ New Checker for JUnit3 Unittests. """

    # Add fields to configure checker instances. You can use any of the Django fields. (See online documentation)
    # The fields created, task, public, required and always will be inherited from the abstract base class Checker
    class_name = models.CharField(
            max_length=100,
            help_text=_("The fully qualified name of the test case class (without .class)")
        )
    test_description = models.TextField(help_text = _("Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded."))
    name = models.CharField(max_length=100, help_text=_("Name of the Testcase. To be displayed as title on Checker Results page"))
    ignore = models.CharField(max_length=4096, help_text=_("space-separated list of files to be ignored during compilation, i.e.: these files will not be compiled."), default="", blank=True)

    JUNIT_CHOICES = (
      ('junit4', 'JUnit 4'),
      ('junit3', 'JUnit 3'),
    )
    junit_version = models.CharField(max_length=16, choices=JUNIT_CHOICES, default="junit3")

    def runner(self):
        return {'junit4' : 'org.junit.runner.JUnitCore', 'junit3' : 'junit.textui.TestRunner' }[self.junit_version]

    def title(self):
        return "JUnit Test: " + self.name

    @staticmethod
    def description():
        return "This Checker runs a JUnit Testcases existing in the sandbox. You may want to use CreateFile Checker to create JUnit .java and possibly input data files in the sandbox before running the JavaBuilder. JUnit tests will only be able to read input data files if they are placed in the data/ subdirectory."

    def output_ok(self, output):
        return (RXFAIL.search(output) == None)

    def run(self, env):
        java_builder = IgnoringJavaBuilder(_flags="", _libs=self.junit_version, _file_pattern=r"^.*\.[jJ][aA][vV][aA]$", _output_flags="", _main_required=False)
        java_builder._ignore = self.ignore.split(" ")


        build_result = java_builder.run(env)

        if not build_result.passed:
            result = self.create_result(env)
            result.set_passed(False)
            result.set_log('<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/>\n'+build_result.log)
            return result

        environ = {}

        environ['UPLOAD_ROOT'] = settings.UPLOAD_ROOT
        environ['JAVA'] = settings.JVM
        script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')
        environ['POLICY'] = os.path.join(script_dir, "junit.policy")
        environ['LANG'] = settings.LANG
        environ['LANGUAGE'] = settings.LANGUAGE

        cmd = [settings.JVM_SECURE, "-cp", settings.JAVA_LIBS[self.junit_version]+":.", self.runner(), self.class_name]
        [output, error, exitcode, timed_out, oom_ed] = execute_arglist(cmd, env.tmpdir(), environment_variables=environ, timeout=settings.TEST_TIMEOUT, fileseeklimit=settings.TEST_MAXFILESIZE, filenumberlimit=settings.TEST_MAXFILENUMBER, extradirs=[script_dir])

        result = self.create_result(env)

        (output, truncated) = truncated_log(output)
        output = '<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/><pre>' + escape(output) + '</pre>'

        #TODO this is just a workaround for the deprecation of Java Security Manager (since java 17)
        # the warnings occur because the java (alias-)script ../scripts/java that is called by Praktomat sets the command line option to use java security manager
        # problem is that these warning occur also in the output of the JUnit-checker and irritate the students
        output = output.replace("WARNING: A command line option has enabled the Security Manager\n","")
        output = output.replace("WARNING: The Security Manager is deprecated and will be removed in a future release\n","")


        result.set_log(output, timed_out=timed_out or oom_ed, truncated=truncated, oom_ed=oom_ed)
        result.set_passed(not exitcode and not timed_out and not oom_ed and self.output_ok(output) and not truncated)
        return result

#class JUnitCheckerForm(AlwaysChangedModelForm):
#    def __init__(self, **args):
#        """ override default values for the model fields """
#        super(JUnitCheckerForm, self).__init__(**args)
#        self.fields["_flags"].initial = ""
#        self.fields["_output_flags"].initial = ""
#        self.fields["_libs"].initial = "junit3"
#        self.fields["_file_pattern"].initial = r"^.*\.[jJ][aA][vV][aA]$"

class JavaBuilderInline(CheckerInline):
    """ This Class defines how the the the checker is represented as inline in the task admin page. """
    model = JUnitChecker
#    form = JUnitCheckerForm

# A more advanced example: By overwriting the form of the checkerinline the initial values of the inherited atributes can be overritten.
# An other example would be to validate the inputfields in the form. (See Django documentation)
#class ExampleForm(AlwaysChangedModelForm):
    #def __init__(self, **args):
        #""" override public and required """
        #super(ExampleForm, self).__init__(**args)
        #self.fields["public"].initial = False
        #self.fields["required"].initial = False

#class ExampleCheckerInline(CheckerInline):
    #model = ExampleChecker
    #form = ExampleForm
