# -*- coding: iso-8859-1 -*-

"""
A C compiler for construction.
"""

from django.conf import settings
from checker.compiler.Builder import Builder
from django.utils.translation import ugettext_lazy as _

class CBuilder(Builder):
	""" A C compiler for construction. """

	# Initialization sets attributes to default values.
	_compiler		= settings.C_BINARY
	_language		= "C"
	#_rx_warnings			= r"^([^ :]*:[^:].*)$"

		
	def flags(self, env):
		if not self.is_MainRequired(env):
			self._flags = self.add_toCompilerFlags("-c", env)
		return super(CBuilder,self).flags(env)
		


from checker.admin import CheckerInline, AlwaysChangedModelForm

class CheckerForm(AlwaysChangedModelForm):
	""" override default values for the model fields """
	def __init__(self, **args):
		super(CheckerForm, self).__init__(**args)
		#self.fields["_flags"].initial = "-Wall"
		#self.fields["_output_flags"].initial = "-o %s"
		#self.fields["_libs"].initial = ""
		self.fields["_file_pattern"].initial = r"^[a-zA-Z0-9_]*\.[cC]$"
		self.fields["_main_required"].label = _("link as executable program")
		self.fields["_main_required"].help_text = _("if not activated, code will be compiled to object file *.o! Compiler uses -c option")
	

class CBuilderInline(CheckerInline):
	model = CBuilder
	form = CheckerForm
	

