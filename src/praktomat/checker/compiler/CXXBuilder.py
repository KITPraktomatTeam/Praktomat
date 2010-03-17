# -*- coding: iso-8859-1 -*-

"""
A C++ compiler for construction.
"""

from django.utils.translation import ugettext_lazy as _
from praktomat.checker.compiler.Builder import Builder
from django.conf import settings

class CXXBuilder(Builder):
	""" A C++ compiler for construction. """
	
	# override configuration
	_compiler				= settings.CXX_BINARY
	_language				= "C++"
	#_rx_warnings			= r"^([^ :]*:[^:].*)$"

from praktomat.checker.admin import CheckerInline
from django.forms import ModelForm

class CheckerForm(ModelForm):
	def __init__(self, **args):
		""" override default values for the model fields """
		super(ModelForm, self).__init__(**args)
		#self.fields["_flags"].initial = "-Wall"
		self.fields["_output_flags"].initial = ""
		#self.fields["_libs"].initial = ""
		# GCC accepts the following extensions for C++ files: ".cc", ".cxx", ".cpp", ".c++", ".C".
		self.fields["_file_pattern"].initial = r"^[a-zA-Z0-9_]*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$"
	
class CXXBuilderInline(CheckerInline):
	model = CXXBuilder
	form = CheckerForm
	