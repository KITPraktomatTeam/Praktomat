# -*- coding: iso-8859-1 -*-

"""
A Scala compiler for construction.
"""

import os, re
from django.conf import settings
from checker.basemodels import Checker
from checker.compiler.Builder import Builder
from checker.compiler.JavaBuilder import ClassFileGeneratingBuilder
from django.template.loader import get_template

class ScalaBuilder(ClassFileGeneratingBuilder):
    """ A Scala compiler. """

    # Initialization sets attributes to default values.
    _compiler = settings.SCALAC
    _language = "scala"

# _rx_warnings			= r"^([^ :]*:[^:].*)$"

    def build_log(self,output,args,filenames):
        t = get_template('checker/compiler/scala_builder_report.html')
        return t.render({'filenames' : filenames, 'output' : output, 'cmdline' : os.path.basename(args[0]) + ' ' +  reduce(lambda parm,ps: parm + ' ' + ps,args[1:],'')})

from checker.admin import CheckerInline, AlwaysChangedModelForm


class CheckerForm(AlwaysChangedModelForm):
    """ override default values for the model fields """

    def __init__(self, **args):
        super(CheckerForm, self).__init__(**args)
        self.fields["_flags"].initial = ""
        self.fields["_output_flags"].initial = ""
        self.fields["_file_pattern"].initial = r"^[A-Z][a-zA-Z0-9_]*\.scala$"
        self.fields["required"].initial = True


class ScalaBuilderInline(CheckerInline):
    model = ScalaBuilder
    form = CheckerForm


