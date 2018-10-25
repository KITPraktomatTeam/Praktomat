# -*- coding: utf-8 -*-

"""
A Haskell compiler.
"""

import os, re
import string
from checker.compiler.Builder import Builder
from django.conf import settings
from django.template.loader import get_template
from django.utils.html import escape

from utilities.safeexec import execute_arglist

class HaskellBuilder(Builder):
	""" A Haskell Compiler """

	# Initialization sets own attributes to default values.
	_compiler	= settings.GHC
	_language	= "Haskell"
	_env            = {}
        _detected_main  = None


	def main_module(self, env):
                if self._detected_main: return self._detected_main
                raise self.NotFoundError("A module Main containing the function main :: IO () could not be found.")

	def libs(self):
		required_libs = super(HaskellBuilder,self).libs()
                return [x for l in [["-package",lib] for lib in required_libs] for x in l]

	def flags(self, env):
                """ Always use -v1, since we grep the output for linked binaries, if any"""
		return (self._flags.split(" ") if self._flags else []) + ["-v1"]

	def build_log(self,output,args,filenames):
		t = get_template('checker/compiler/haskell_builder_report.html')
		return t.render({'filenames' : filenames, 'output' : output, 'cmdline' : os.path.basename(args[0]) + ' ' +  reduce(lambda parm,ps: parm + ' ' + ps,args[1:],'')})

	def run(self, env):
		""" Build it. """
		result = self.create_result(env)

		filenames = [name for name in self.get_file_names(env)]
		args = [self.compiler()] + self.flags(env) + filenames + self.libs()
		[output,_,_,_,_]  = execute_arglist(args, env.tmpdir(),self.environment())

                has_main = re.search(r"^Linking ([^ ]*) ...$",output,re.MULTILINE)
                if has_main: self._detected_main = has_main.group(1)

		output = escape(output)
		output = self.enhance_output(env, output)

		# We mustn't have any warnings.
		passed = not self.has_warnings(output)	
		log  = self.build_log(output,args,set(filenames).intersection([solutionfile.path() for solutionfile in env.solution().solutionfile_set.all()]))

		# Now that submission was successfully built, try to find the main modules name again
		try:
			if passed : env.set_program(self.main_module(env))
		except self.NotFoundError as e:
			passed = not self._main_required
			log += "<pre>" + str(e) + "</pre>"

		result.set_passed(passed)
		result.set_log(log)
		return result        

from checker.admin import CheckerInline, AlwaysChangedModelForm

class CheckerForm(AlwaysChangedModelForm):
	def __init__(self, **args):
		""" override default values for the model fields """
		super(CheckerForm, self).__init__(**args)
		self.fields["_flags"].initial = "-XSafe"
		self.fields["_output_flags"].initial = ""
		#self.fields["_libs"].initial = ""
		self.fields["_file_pattern"].initial = r"^.*\.[hH][sS]$"
	
class HaskellBuilderInline(CheckerInline):
	model = HaskellBuilder
	form = CheckerForm
	
