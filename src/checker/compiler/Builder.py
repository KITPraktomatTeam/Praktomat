# -*- coding: utf-8 -*-

import os
from pipes import quote
import re, subprocess
import shlex
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from django.template.loader import get_template


from checker.basemodels import Checker
from utilities.safeexec import execute_arglist
from functools import reduce

class Builder(Checker):
    """ Build a program. This contains the general infrastructure to build a program with a compiler.  Specialized subclass are provided for different languages and compilers. """

    class Meta(Checker.Meta):
        abstract = True

    # builder configuration. override in subclass
    _compiler                = "gcc"                        # command to invoke the compiler in the shell
    _language                = "konfigurierbar"            # the language of the compiler, e.g. C++ or Java
    _rx_warnings            = r"^([^:]*:[^:].*)$"        # Regular expression describing warnings and errors in the output of the compiler
    _env                            = {}


    _flags              = models.CharField(max_length = 1000, blank = True, default="-Wall", help_text = _('Compiler flags'))
    _output_flags      = models.CharField(max_length = 1000, blank = True, default ="-o %s", help_text = _('Output flags. \'%s\' will be replaced by the program name.'))
    _libs              = models.CharField(max_length = 1000, blank = True, default = "", help_text = _('Compiler libraries'))
    _file_pattern      = models.CharField(max_length = 1000, default = r"^[a-zA-Z0-9_]*$", help_text = _('Regular expression describing all source files to be passed to the compiler.'))
    _main_required    = models.BooleanField(default = True, help_text = _('Is a submission required to provide a main method?'))

    def title(self):
        return "%s - Compiler" % self.language()

    @staticmethod
    def description():
        return "Diese Prüfung ist bestanden, wenn der Compiler das Programm ohne Fehler oder Warnungen übersetzt."

    def compiler(self):
        """ Compiler name. To be overloaded in subclasses. """
        return self._compiler

    def flags(self, env):
        """ Compiler flags.    To be overloaded in subclasses. """
        return self._flags.split(" ") if self._flags else []

    def output_flags(self, env):
        """ Output flags """
        try:
            return shlex.split(self._output_flags % '"'+env.program()+'"')
        except:
            return self._output_flags.split(" ") if self._output_flags else []

    def libs(self):
        """ Compiler libraries.     To be overloaded in subclasses. """
        return self._libs.split(" ") if self._libs else []

    def environment(self):
        """ Environment to be set on onvocation of Compiler. """
        return self._env

    def language(self):
        """ Language.  To be overloaded in subclasses """
        return self._language

    def rxarg(self):
        """ Regexp for compile command argument.  Files that do not match this regexp will be uploaded,
            but not passed as argument to the compiler     (such as header files in C/C++).
            This also protects somewhat against options (`-foo') and metacharacters (`foo; ls') in file names. To be overloaded in subclasses. """
        return self._file_pattern

    def get_file_names(self, env):
        rxarg = re.compile(self.rxarg())
        return [name for (name, content) in env.sources() if rxarg.match(name)]

    def exec_file(self, tmpdir, program_name):
        """ File of the generated executable.  To be overloaded in subclasses. """
        return os.path.join(tmpdir, program_name)

    def enhance_output(self, env, output):
        """ Add more info to build output OUTPUT.  To be overloaded in subclasses. """
        return re.sub(re.compile(self._rx_warnings, re.MULTILINE), r"<b>\1</b>", output)

    def has_warnings(self, output):
        """ Return true if there are any warnings in OUTPUT """
        return re.compile(self._rx_warnings, re.MULTILINE).search(output) != None

    class NotFoundError(Exception):
            def __init__(self, description):
                self.description = description
            def __str__(self):
                return self.description

    def main_module(self, env):
        """ Creates the name of the main module from the (first) source file name. """
        for module_name in self.get_file_names(env):
            try:
                return module_name[:module_name.index('.')]
            except ValueError:
                pass
        # Module name not found

        raise self.NotFoundError("The main module could not be found.\n")

    def run(self, env):
        """ Build it. """
        result = self.create_result(env)

        # Try to find out the main modules name with only the source files present
        if self._main_required:
            try:
                env.set_program(self.main_module(env))
            except self.NotFoundError:
                pass

        filenames = [name for name in self.get_file_names(env)]
        args = [self.compiler()] + self.output_flags(env) + self.flags(env) + filenames + self.libs()
        script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')
        [output, _, _, _, _]  = execute_arglist(args, env.tmpdir(), self.environment(), extradirs=[script_dir])

        output = escape(output)
        output = self.enhance_output(env, output)

        # We mustn't have any warnings.
        passed = not self.has_warnings(output)
        log  = self.build_log(output, args, set(filenames).intersection([solutionfile.path() for solutionfile in env.solution().solutionfile_set.all()]))

        # Now that submission was successfully built, try to find the main modules name again
        if self._main_required and passed:
            try:
                env.set_program(self.main_module(env))
            except self.NotFoundError as e:
                log += "<pre>" + str(e) + "</pre>"
                passed = False

        result.set_passed(passed)
        result.set_log(log)
        return result

    def build_log(self, output, args, filenames):
        t = get_template('checker/compiler/builder_report.html')
        return t.render({
            'filenames' : filenames,
            'output' : output,
            'cmdline' : os.path.basename(args[0]) + ' ' +  reduce(lambda parm, ps: parm + ' ' + ps, args[1:], ''),
            'regexp' : self.rxarg()
        })
