# -*- coding: utf-8 -*-

"""
A C compiler for construction.
"""

from django.conf import settings
from checker.compiler.Builder import Linker 
from checker.compiler.Builder import IncludeHelper
from checker.compiler.Builder import LibraryHelper
from checker.compiler.Builder import MainNeedHelper

import os, re
from utilities.safeexec import execute_arglist

from django.utils.translation import ugettext_lazy as _

class CLinker(Linker, IncludeHelper, LibraryHelper, MainNeedHelper):
	""" A C compiler for construction. """

	# Initialization sets attributes to default values.
	_linker			= settings.C_BINARY
	_OBJECTINSPECTOR	= "findMainInObject" # shell script name in folder scripts calling nm
	_OBJINSPECT_PAR		= "-A -C"
	_language		= "C"
	#_rx_warnings			= r"^([^ :]*:[^:].*)$"


	def main_search(self,env):
		""" returns module name if main is found in object file """
  		main_symbol = "main"
  		#output of nm -A -C  mytest.o is: mytest.o:0000000d T main
		nm_rx  = re.compile(r"^(.*\.)[oO]:[0-9A-Fa-f]* T (main)$", re.MULTILINE)
		obj_files = []
                c_rx = re.compile('^(.*\.)[cC]')
		#ToDo: code review 
		o_solution_list = [c_rx.sub(r"\So", name)\
			for (name,void) in env.sources()\
			if name.endswith(('.c','.C'))]

		for dirpath, dirs, files in os.walk(env.tmpdir()):
			for filename in files:
				if filename.endswith(('.O', '.o')):
				        #ToDo: code review 
					#if object file corresponds to a student uploaded solution file
					if filename in o_solution_list:
						obj_files.append(filename)
						# Next let's shell out and search in object file for main 
						script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'scripts')
						cmd = [os.path.join(script_dir, _OBJECTINSPECTOR), _OBJINSPECT_PAR , os.path.join(dirpath,filename)]
						[objinfo,error,exitcode,timed_out,oom_ed]  = execute_arglist(cmd , env.tmpdir(), self.environment(), timeout=settings.TEST_TIMEOUT, fileseeklimit=settings.TEST_MAXFILESIZE, extradirs=[script_dir])
						if string.find(objinfo,main_symbol) >= 0:
							self.main_object_name = nm_rx.search(objinfo, re.MULTILINE).group(1)
							return self.main_object_name

		raise self.NotFoundError("An object containing the main symbol (i.e. 'int main(int argc, char* argv[])' ) could not be found in the files %s" % ", ".join(obj_files))


# todo: code review	
	def main_module(self,env);
		return self.main_object_name if self.main_object_name else main_search(env)



	def pre_run(self,env):
		return self.linker()



	def post_run(self,env):
		passed = True
		log = ""
		try:
			self.main_module(env)
				
		except self.NotFoundError as e:
			log +=  str(e)
			# But only complain if the main method is required
			if self.main_required():
				log = "Error: " + log                              			
				passed = False
			else:			
				passed = True
				log = "Info: " + log

		return [passed,log]


	def connected_flags(self, env):     		
		return self.flags(env) + self.search_path() + self.libs()




from checker.admin import CheckerInline, AlwaysChangedModelForm

class CheckerForm(AlwaysChangedModelForm):
  
	""" override default values for the model fields """
	def __init__(self, **args):
		super(CheckerForm, self).__init__(**args)
		self.fields["_flags"].initial = "-Wl,--warn-common"
		#self.fields["_output_flags"].initial = "-o %s"	
		#self.fields["_output_flags"].default = "-o %s"
		#self.fields["_output_flags"].choices = _LINK_CHOICES	
		#self.fields["_output_flags"].help_text = _('\'%s\' will be replaced by the output name.')
		self.fields["_libs"].initial = ""
		self.fields["_file_pattern"].initial = r"^[a-zA-Z0-9_]*\.[oO]$"
		self.fields["_main_required"].label = _("link as executable program")
		self.fields["_main_required"].help_text = _("if not activated, object files code will be compiled to object file *.o! Compiler uses -c option")
	

class CBuilderInline(CheckerInline):
	model = CBuilder
	form = CheckerForm
	

