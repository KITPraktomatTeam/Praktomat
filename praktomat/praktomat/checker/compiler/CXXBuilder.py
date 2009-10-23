# -*- coding: iso-8859-1 -*-

"""
A C++ compiler for construction.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from praktomat.checker.models import Builder
from django.conf import settings

class CXXBuilder(Builder):
	""" A C++ compiler for construction. """
	
	# override configuration
	_compiler				= settings.CXX_BINARY
	_language				= "C++"
	#_rx_warnings			= r"^([^ :]*:[^:].*)$"
	
	_flags			= models.CharField(max_length = 1000, blank = True, default = "-Wall", help_text = _('Compiler flags')) 
	_output_flags	= models.CharField(max_length = 1000, blank = True, default = "", help_text = _('Output flags. \'%s\' will be replaced by the program name.'))
	_libs			= models.CharField(max_length = 1000, blank = True, default = "", help_text = _('Compiler libraries'))
	_file_pattern	= models.CharField(max_length = 1000, default = r"^[a-zA-Z0-9_]*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$", help_text = _('Regular expression describing all source files to be passed to the compiler.'))
	
#	# override default values for the model fields
#	defaults['flags']			= "-Wall", # -static"
#	defaults['output_flags']	= ""
#	defaults['libs']			= ""
#	# GCC accepts the following extensions for C++ files:
#	# ".cc", ".cxx", ".cpp", ".c++", ".C".
#	# All other file names (including .o) are passed to the linker.
#	defaults['file_pattern']	= r"^[a-zA-Z0-9_]*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$"

from praktomat.checker.admin import	AllDefaultCheckerInline
class CXXBuilderInline(AllDefaultCheckerInline):
	model = CXXBuilder