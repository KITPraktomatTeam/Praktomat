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

from utilities.safeexec import execute_arglist

class JavaBuilder(Builder):
	"""	 A Java bytecode compiler for construction. """

	# Initialization sets own attributes to default values.
	_compiler	= settings.JAVA_BINARY_SECURE
	_language	= "Java"
	_env            = {}
	_env['JAVAC'] = settings.JAVA_BINARY
	_env['JCFDUMP'] = settings.JCFDUMP

	def main_module(self, env):
		""" find the first class file containing a main method """
		main_method = "public static void main(java.lang.String[])"
		class_name  = re.compile(r"^(public )?(abstract )?(final )?class ([^ ]*)( extends .*)? \{$", re.MULTILINE)
		class_files = []
		for dirpath, dirs, files in os.walk(env.tmpdir()):
			for filename in files:
				if filename.endswith(".class"):
					class_files.append(filename)
					[classinfo,_,_,_,_]  = execute_arglist([settings.JAVAP, os.path.join(dirpath,filename)], env.tmpdir(), self.environment(), unsafe=True)
					if string.find(classinfo,main_method) >= 0:
						main_class_name = class_name.search(classinfo, re.MULTILINE).group(4)
						return main_class_name

		raise self.NotFoundError("A class containing the main method ('public static void main(String[] args)') could not be found in the files %s" % ", ".join(class_files))


	def libs(self):
		def toPath(lib):
			if lib=="junit3":
				 return settings.JUNIT38_JAR
			return lib 

		required_libs = super(JavaBuilder,self).libs()

		return ["-cp",".:"+(":".join([ settings.JAVA_LIBS[lib] for lib in required_libs if lib in settings.JAVA_LIBS ]))]
		#return ["-cp",".:/opt/praktomat-addons/org.eclipse.jdt.core-3.10.0.jar:/opt/praktomat-addons/org.eclipse.equinox.common-3.6.0.jar:/opt/praktomat-addons/hamcrest-core-1.3.jar:/opt/praktomat-addons/org.eclipse.core.resources-3.7.100.jar:/opt/praktomat-addons/org.eclipse.core.expressions-3.4.300.jar:/opt/praktomat-addons/praktomat.utilities-1.jar:/opt/praktomat-addons/filesystem-1.1.0-v20070606.jar:/opt/praktomat-addons/org.eclipse.text-3.5.101.jar:/opt/praktomat-addons/app-1.3.200-v20130910-1609.jar:/opt/praktomat-addons/preferences-3.5.200-v20140224-1527.jar:/opt/praktomat-addons/jobs-3.6.0-v20140424-0053.jar:/opt/praktomat-addons/org.eclipse.core.jobs-3.5.0.v20100515.jar:/opt/praktomat-addons/registry-3.5.400-v20140428-1507.jar:/opt/praktomat-addons/contenttype-3.4.200-v20140207-1251.jar:/opt/praktomat-addons/org.eclipse.core.contenttype-3.4.100.v20100505-1235.jar:/opt/praktomat-addons/osgi-3.10.0-v20140606-1445.jar:/opt/praktomat-addons/org.eclipse.equinox.preferences-3.3.0.v20100503.jar:/opt/praktomat-addons/org.eclipse.equinox.app-1.3.100.jar:/opt/praktomat-addons/resources-3.3.0-v20070604.jar:/opt/praktomat-addons/expressions-3.3.0-v20070606-0010.jar:/opt/praktomat-addons/org.eclipse.core.commands-3.6.0.jar:/opt/praktomat-addons/junit-4.12.jar:/opt/praktomat-addons/runtime-3.10.0-v20140318-2214.jar:/opt/praktomat-addons/org.eclipse.core.runtime-3.7.0.jar:/opt/praktomat-addons/org.eclipse.equinox.registry-3.5.0.v20100503.jar:/opt/praktomat-addons/org.eclipse.osgi-3.7.1.jar:/opt/praktomat-addons/common-3.6.200-v20130402-1505.jar:/opt/praktomat-addons/org.eclipse.core.filesystem-1.3.100.jar"]

	def flags(self, env):
		""" Accept unicode characters. """
		return (self._flags.split(" ") if self._flags else []) + ["-encoding", "utf-8"]

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
	
