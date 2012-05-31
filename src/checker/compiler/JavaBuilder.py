# -*- coding: utf-8 -*-

"""
A Java bytecode compiler for construction.
"""

import os, re
import string
from checker.compiler.Builder import Builder
from django.conf import settings
from django.template.loader import get_template
from django.template import Context


class JavaBuilder(Builder):
	"""	 A Java bytecode compiler for construction. """

	# Initialization sets own attributes to default values.
	_compiler	= settings.JAVA_BINARY_SECURE
	_language	= "Java"
	_env            = {}
	_env['JAVAC'] = settings.JAVA_BINARY
	_env['JCFDUMP'] = settings.JCFDUMP

	def main_module(self, env):
		""" find the first source code file containing a main method """
		file_name_filter = re.compile(self.rxarg())
		# public static void main(String[] args) or public static void main(String... args)
		# allow variable spacing, ignore case and allow for other parameter names than args
		main_method_regex = re.compile(r"public\s+static\s+void\s+main\s*\(\s*(final\s*)?String\s*(\[\]|\.\.\.)\s*\S*\s*\)", re.IGNORECASE)
		for (name,content) in  env.sources():
			if file_name_filter.match(name) and main_method_regex.search(content):
				# convert file to class name
				chopped = name[:-len(".java")]
				(head, result) = os.path.split(chopped)
				while head != "":
					chopped = string.join((head, result), ".")
					(head, result) = os.path.split(chopped)			
				return result
		raise self.NotFoundError("The class containing the main method('public static void main(String[] args)') could not be found.")


	def libs(self):
		def toPath(lib):
			if lib=="junit3":
				 return settings.JUNIT38_JAR
			return lib 

		required_libs = super(JavaBuilder,self).libs()

		return ["-cp ",".:"+(":".join([ settings.JAVA_LIBS[lib] for lib in required_libs if lib in settings.JAVA_LIBS ]))]

	def flags(self, env):
		""" Accept unicode characters. """
		return self._flags.split(" ") + ["-encoding", "utf-8"]

	def build_log(self,output,args,filenames):
		t = get_template('checker/compiler/java_builder_report.html')
		return t.render(Context({'filenames' : filenames, 'output' : output, 'cmdline' : os.path.basename(args[0]) + ' ' +  reduce(lambda parm,ps: parm + ' ' + ps,args[1:],'')}))

from checker.admin import CheckerInline, AlwaysChangedModelForm

class CheckerForm(AlwaysChangedModelForm):
	def __init__(self, **args):
		""" override default values for the model fields """
		super(CheckerForm, self).__init__(**args)
		self.fields["_flags"].initial = ""
		self.fields["_output_flags"].initial = ""
		#self.fields["_libs"].initial = ""
		self.fields["_file_pattern"].initial = r"^.*\.[jJ][aA][vV][aA]$"
	
class JavaBuilderInline(CheckerInline):
	model = JavaBuilder
	form = CheckerForm
	
