# -*- coding: iso-8859-1 -*-

"""
A C compiler for construction.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from praktomat.checker.models import Builder
from django.conf import settings

class CBuilder(Builder):
	""" A C compiler for construction. """

	# Initialization sets attributes to default values.
	_compiler		= settings.C_BINARY
	_language		= "C"
	#_pattern		= "*.[ch]"
		
	_flags			= models.CharField(max_length = 1000, blank = True, default = "-Wall", help_text = _('Compiler flags')) 
	_output_flags	= models.CharField(max_length = 1000, blank = True, default = "-o %s", help_text = _('Output flags. \'%s\' will be replaced by the program name.'))
	_libs			= models.CharField(max_length = 1000, blank = True, default = "", help_text = _('Compiler libraries'))
	_file_pattern	= models.CharField(max_length = 1000, default = r"^[a-zA-Z0-9_]*\.[cC]$", help_text = _('Regular expression describing all source files to be passed to the compiler.'))

from praktomat.checker.admin import	AllDefaultCheckerInline
class CBuilderInline(AllDefaultCheckerInline):
	model = CBuilder