# -*- coding: utf-8 -*-

"""
Dump files containing input, expected output and the shell script running diff.
"""

import os
import os.path

from django.db import models
from django.utils.translation import ugettext_lazy as _
from checker.models import Checker, CheckerFileField, CheckerResult, execute_arglist
from django.utils.html import escape
from utilities.file_operations import *

class DiffChecker(Checker):

    shell_script = CheckerFileField(help_text=_("The shell script whose output for the given input file is compared to the given output file."))
    input_file = CheckerFileField(blank=True, help_text=_("The file containing the input for the program."))
    output_file = CheckerFileField(blank=True, help_text=_("The file containing the output for the program."))
    
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
        copy_file_to_directory(self.shell_script.path, test_dir, replace=replace)
        args = ["sh",  os.path.basename(self.shell_script.name)]
        #environ['USER'] = unicode(env.user().get_full_name()).encode('utf-8')
        environ['USER'] = env.user().username # gets overwritten with praktomat-test-user's name, therefore:
        environ['AUTHOR'] = env.solution().author.username # will not be overwritten!
        environ['HOME'] = test_dir
        
        [output, error, exitcode,_] = execute_arglist(args, working_directory=test_dir, environment_variables=environ)
        
        result = CheckerResult(checker=self)

        result.set_log('<pre>' + escape(output) + '</pre>')
        result.set_passed(not exitcode)
        
        return result
    

from checker.admin import    CheckerInline

class DiffCheckerInline(CheckerInline):
    model = DiffChecker
