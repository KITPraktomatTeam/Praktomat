# -*- coding: iso-8859-1 -*-

"""
A C compiler for construction.
"""

from django.conf import settings
from praktomat.checker.compiler.Builder import Builder

class CBuilder(Builder):
	""" A C compiler for construction. """

	# Initialization sets attributes to default values.
	_compiler		= settings.C_BINARY
	_language		= "C"
	#_rx_warnings			= r"^([^ :]*:[^:].*)$"



from praktomat.checker.admin import CheckerInline, addChangedFieldForm

class CheckerForm(addChangedFieldForm):
	""" override default values for the model fields """
	def __init__(self, **args):
		super(addChangedFieldForm, self).__init__(**args)
		#self.fields["_flags"].initial = "-Wall"
		#self.fields["_output_flags"].initial = "-o %s"
		#self.fields["_libs"].initial = ""
		self.fields["_file_pattern"].initial = r"^[a-zA-Z0-9_]*\.[cC]$"
	
class CBuilderInline(CheckerInline):
	model = CBuilder
	form = CheckerForm
	

