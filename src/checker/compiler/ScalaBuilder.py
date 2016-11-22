# -*- coding: iso-8859-1 -*-

"""
A Scala compiler for construction.
"""

from django.conf import settings
from checker.basemodels import Checker
from checker.compiler.Builder import Builder


class ScalaBuilder(Builder):
    """ A C compiler for construction. """

    # Initialization sets attributes to default values.
    _compiler = settings.SCALA
    _language = "scala"

# _rx_warnings			= r"^([^ :]*:[^:].*)$"


from checker.admin import CheckerInline, AlwaysChangedModelForm


class CheckerForm(AlwaysChangedModelForm):
    """ override default values for the model fields """

    def __init__(self, **args):
        super(CheckerForm, self).__init__(**args)
        self.fields["_flags"].initial = ""
        self.fields["_output_flags"].initial = "-o %s"
        self.fields["_file_pattern"].initial = r"^[A-Z][a-zA-Z0-9_]*\.scala$"
        self.fields["required"].initial = True


class ScalaBuilderInline(CheckerInline):
    model = ScalaBuilder
    form = CheckerForm


