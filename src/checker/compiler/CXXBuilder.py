# -*- coding: iso-8859-1 -*-

"""
A C++ compiler for construction.
"""

from django.utils.translation import ugettext_lazy as _
from checker.compiler.Builder import Compiler
from django.conf import settings

class CXXBuilder(Compiler):
	""" A C++ compiler for construction. """
	
	# override configuration
	_compiler			= settings.CXX_BINARY
	_language			= "C++"
	#_rx_warnings			= r"^([^ :]*:[^:].*)$"

	def pre_run(self,env):
		return self.compiler()



	def post_run(self,env):
		passed = True
		log = ""
		return [passed,log]


	def connected_flags(self, env):     		
		return self.flags(env) + self.search_path()


from checker.admin import CheckerInline, AlwaysChangedModelForm

class CheckerForm(AlwaysChangedModelForm):
	def __init__(self, **args):
		""" override default values for the model fields """
		super(CheckerForm, self).__init__(**args)
		self.fields["_flags"].initial = "-Wall -Wextra"
		#self.fields["_output_flags"].initial = "-o %s"
		self.fields["_output_flags"].initial = "-c"
		#self.fields["_libs"].initial = ""
		# GCC accepts the following extensions for C++ files: ".cc", ".cxx", ".cpp", ".c++", ".C".
		self.fields["_file_pattern"].initial = r"^[a-zA-Z0-9_]*\.(c|C|cc|CC|cxx|CXX|c\+\+|C\+\+|cpp|CPP)$"
		#self.fields["_main_required"].label = _("Link as executable program.")
		#self.fields["_main_required"].help_text = _("if not activated, code will be compiled to object file *.o ! Compiler uses -c option")


class CXXBuilderInline(CheckerInline):
	model = CXXBuilder
	form = CheckerForm
	verbose_name = "C++ Compiler"