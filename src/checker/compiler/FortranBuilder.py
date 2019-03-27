# -*- coding: iso-8859-1 -*-

"""
A FORTRAN compiler for construction.
"""

from django.conf import settings
from checker.compiler.Builder import Builder

class FortranBuilder(Builder):
    """ A FORTRAN compiler for construction. """

    # Initialization sets attributes to default values.
    _compiler        = settings.FORTRAN_BINARY
    _language        = "FORTRAN 77"
    #_rx_warnings    = r"^([^ :]*:[^:].*)$"



from checker.admin import CheckerInline, AlwaysChangedModelForm

class CheckerForm(AlwaysChangedModelForm):
    """ override default values for the model fields """
    def __init__(self, **args):
        super(CheckerForm, self).__init__(**args)
        self.fields["_flags"].initial = "-Wall -static"
        #self.fields["_output_flags"].initial = "-o %s"
        #self.fields["_libs"].initial = ""
        self.fields["_file_pattern"].initial = r"^[a-zA-Z0-9_]*\.(f|F|for|FOR)$"

class FortranBuilderInline(CheckerInline):
    model = FortranBuilder
    form = CheckerForm
