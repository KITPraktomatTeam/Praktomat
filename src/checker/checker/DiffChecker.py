# -*- coding: utf-8 -*-

"""
Dump files containing input, expected output and the shell script running diff.
"""

import os, re

import os.path

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
#from django.utils.encoding import force_unicode
from checker.basemodels import Checker, CheckerFileField, CheckerResult, truncated_log
from django.core.exceptions import ValidationError
from utilities.safeexec import execute_arglist
from utilities.file_operations import *




class DiffChecker(Checker):

    shell_script = CheckerFileField(help_text=_("The shell script whose output for the given input file is compared to the given output file: The substrings JAVA and PROGRAM got replaced by Praktomat determined values."))
    input_file = CheckerFileField(blank=True, help_text=_("The file containing the input for the program."))
    output_file = CheckerFileField(blank=True, help_text=_("The file containing the output for the program."))


    def clean(self):
        super(DiffChecker, self).clean()
        if (not self.shell_script or not self.input_file or not self.output_file): raise ValidationError("Robert says: DiffChecker have to have an Shell script, an Inputfile and an Outputfile")

    def title(self):
        """ Returns the title for this checker category. """
        return u"Ausgaben mit 'diff' prüfen."

    @staticmethod
    def description():
        """ Returns a description for this Checker. """
        return u"Diese Prüfung wird bestanden, wenn erwartete und tatsächliche Ausgabe übereinstimmen."

    def run(self, env):
        """ Runs tests in a special environment. Here's the actual work.
        This runs the check in the environment ENV, returning a CheckerResult. """

        # Setup
        test_dir     = env.tmpdir()
        environ = {}
        if self.input_file:
            input_path = os.path.join(test_dir, os.path.basename(self.input_file.path))
            environ['INPUTFILE'] = os.path.basename(self.input_file.path)
            copy_file(self.input_file.path, input_path)
        if self.output_file:
            output_path = os.path.join(test_dir, os.path.basename(self.output_file.path))
            environ['OUTPUTFILE'] = os.path.basename(self.output_file.path)
            copy_file(self.output_file.path, output_path)
        replace = [(u'PROGRAM',env.program())] if env.program() else []
        replace +=[("JAVA",settings.JVM_SECURE)]
        #copy_file_to_directory(self.shell_script.path, test_dir, replace=replace)
        copy_file(self.shell_script.path, test_dir, to_is_directory=True)

        #some time after 2013 Praktomat losts copy_file_to_directory with replace parameter
        to_path = os.path.join(test_dir, os.path.basename(self.shell_script.path))
        with open(to_path) as fd:
                content = encoding.get_unicode(fd.read())
                for (old, new) in replace:
                        content = content.replace(old, new)
        with open(to_path, 'w') as fd:
                fd.write(encoding.get_utf8(content))


        args = ["sh",  os.path.basename(self.shell_script.name)]
        #environ['USER'] = unicode(env.user().get_full_name()).encode('utf-8')
        environ['USER'] = env.user().username # gets overwritten with praktomat-test-user's name, therefore:
        environ['AUTHOR'] = env.solution().author.username # will not be overwritten!
        environ['HOME'] = test_dir

        script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'scripts')

        #[output, error, exitcode,_] = execute_arglist(args, working_directory=test_dir, environment_variables=environ)

        [output, error, exitcode,timed_out, oom_ed] = execute_arglist(
                            args,
                            working_directory=test_dir,
                            environment_variables=environ,
                            timeout=settings.TEST_TIMEOUT,
                            maxmem=settings.TEST_MAXMEM,
                            fileseeklimit=settings.TEST_MAXFILESIZE,
                            filenumberlimit=settings.TEST_MAXFILENUMBER,
                            extradirs = [script_dir],
                            )
        output = force_unicode(output, errors='replace')
        #TODO this is just a workaround for the deprecation of Java Security Manager (since java 17)
        # the warnings occur because the java (alias-)script ../scripts/java that is called by Praktomat sets the command line option to use java security manager
        # problem is that these warning occur also in the output of the JUnit-checker and irritate the students
        output = output.replace("WARNING: A command line option has enabled the Security Manager\n","")
        output = output.replace("WARNING: The Security Manager is deprecated and will be removed in a future release\n","")

        result = CheckerResult(checker=self, solution=env.solution())

        result.set_log('<pre>' + escape(output) + '</pre>')

        result.set_passed(not exitcode)

        return result


from checker.admin import    CheckerInline

class DiffCheckerInline(CheckerInline):
    model = DiffChecker
