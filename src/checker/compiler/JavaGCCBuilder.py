# -*- coding: iso-8859-1 -*-

"""
A Java native compiler for construction.
"""

from django.conf import settings
from checker.compiler.Builder import Builder

class JavaGCCBuilder(Builder):
    """ A C compiler for construction. """

    # Initialization sets attributes to default values.
    _compiler        = settings.JAVA_GCC_BINARY
    _language        = "Java/GCC"
    #_rx_warnings    = r"^([^ :]*:[^:].*)$"



from checker.admin import CheckerInline, AlwaysChangedModelForm

class CheckerForm(AlwaysChangedModelForm):
    """ override default values for the model fields """
    def __init__(self, **args):
        super(CheckerForm, self).__init__(**args)
        self.fields["_flags"].initial = "-Wall -static"
        self.fields["_output_flags"].initial = "--main=%s"
        #self.fields["_libs"].initial = ""
        self.fields["_file_pattern"].initial = r"^[a-zA-Z0-9_]*\.[jJ][aA][vV][aA]$"

class JavaGCCBuilderInline(CheckerInline):
    model = JavaGCCBuilder
    form = CheckerForm