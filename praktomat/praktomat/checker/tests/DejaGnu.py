# -*- coding: utf-8 -*-

"""
DejaGnu Tests.
"""

import os
import string
import re
import time
import subprocess

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from praktomat.checker.models import Checker, Builder, CheckerResult, TMP_DIR_MODE

# Stuff to highlight in output
RXFAIL	   = re.compile(r"^(.*)(FAIL|ERROR|Abort|Exception |your program crashed|cpu time limit exceeded|"
						"ABBRUCH DURCH ZEITUEBERSCHREITUNG|# of unexpected failures.*[0-9]+)(.*)$",	re.MULTILINE)
RXPASS	   = re.compile(r"^(.*)(PASS)(.*)$", re.MULTILINE)
RXRUN_BY   = re.compile(r"Run By .* on ")

# Stuff to remove from output
RXREMOVE   = re.compile(r"(Schedule of variations:.*interface file.)|(Running \./[ -z]*/[a-z]*\.exp \.\.\.)", re.DOTALL)

class DejaGnu:
	""" Common superclass for all DejaGnu-related stuff. """
	
	# Directories
	def testsuite_dir(self, env):
		return os.path.join(env.tmpdir(), "testsuite")

	def config_dir(self, env):
		return os.path.join(self.testsuite_dir(env), "config")

	def lib_dir(self, env):
		return os.path.join(self.testsuite_dir(env), "lib")

	def tests_dir(self, env):
		return os.path.join(self.testsuite_dir(env), env.program() + ".tests")

	def setup_dirs(self, env):
		os.mkdir(self.testsuite_dir(env), TMP_DIR_MODE)
		os.mkdir(self.config_dir(env),	  TMP_DIR_MODE)
		os.mkdir(self.lib_dir(env),		  TMP_DIR_MODE)
		os.mkdir(self.tests_dir(env),	  TMP_DIR_MODE)
	


class DejaGnuTester(Checker, DejaGnu):
	""" Run a test case on the program.  Requires a previous `DejaGnuSetup'. """	
	
	name = models.CharField(max_length=100, help_text=_("The name of the Test"))
	test_case = models.FileField(upload_to="AdminFiles/DejaGnuTestCases/%Y%m%d%H%M%S/", help_text=_(u"In den folgenden DejaGnu-Testfällen werden typischerweise Funktionen aufgerufen, die beim vorherigen Schritt <EM>Tests einrichten</EM> definiert wurden.	 Siehe	auch den Abschnitt <EM>How to write a test case</EM> im <A TARGET=\"_blank\" HREF=\"http://www.gnu.org/manual/dejagnu/\">DejaGnu-Handbuch</A>."))

	def __unicode__(self):
		return self.name
	
	def title(self):
		return self.name
		
	def description(self):
		return u"Diese Prüfung ist bestanden, wenn alle Testfälle zum erwarteten Ergebnis führten."

	def requires(self):
		return [ DejaGnuSetup ]

	# Return 1 if the output is ok
	def output_ok(self, output):
		return (RXFAIL.search(output) == None and
				string.find(output, "runtest completed") >= 0 and 
				string.find(output, "non-expected failures") < 0 and
				string.find(output, "unexpected failures") < 0)

	def htmlize_output(self, log):
		# Always kill the author's name from the log
		log = re.sub(RXRUN_BY, "Run By " + Site.objects.get_current().name + " on ", log)

		# Clean the output
		log = re.sub(RXREMOVE, "", log)

		# HTMLize it all
		# log = htmlize(log)
		
		# Every line that contains a passed message is to be enhanced.
		log = re.sub(RXPASS, r"\1 <B class=\"pass\"> \2 </B> \3", log)
		# Every line that contains a failure message is to be enhanced.
		return  "<TT><PRE>" + re.sub(RXFAIL, r"\1 <B class=\"fail\"> \2 </B> \3", log) + "</PRE></TT>"


	# Run tests.  Return a CheckerResult.
	def run(self, env):

		# Save public test cases in `tests.exp'
		tests_exp = os.path.join(self.tests_dir(env), "tests.exp")
		fd = open(tests_exp, 'w')
		test_cases = string.replace(self.test_case.read(),"PROGRAM", env.program())
		fd.write(test_cases)
		fd.close()
		
		testsuite = self.testsuite_dir(env)
		program_name = env.program()
		
		args = ["--tool " + program_name, "tests.exp"]
		environ = os.environ # needs testing
		environ['USER'] = env.user().get_full_name() # sh_quote removed
		environ['HOME'] = testsuite
		# needs timeout!
		[output, error] = subprocess.Popen(args, executable = "runtest", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=testsuite, env=environ).communicate()

		try:
			summary = open(os.path.join(testsuite, program_name + ".sum")).read()
			log		= open(os.path.join(testsuite, program_name + ".log")).read()
		except:
			summary = ""
			log		= ""

		complete_output = output + log
		if error:
			complete_output += "ERROR: Ein TimeOut ist aufgetreten!" # Or propably somsing else happend???????
		
		result = self.result()
		result.set_log(self.htmlize_output(complete_output))
		result.set_passed((not error) & self.output_ok(complete_output))
		return result


# A template for test cases.
DEFAULT_TEST_CASES = """# `tests.exp' template
# Insert test cases in the format
# PROGRAM_test "[input]" "[expected_output]"
"""

class DejaGnuSetup(Checker, DejaGnu):

	test_defs = models.FileField(upload_to="AdminFiles/DejaGnuTestCases/%Y%m%d%H%M%S/", help_text=_(u"Das Setup benutzt den <A HREF=\"http://www.gnu.org/software/dejagnu/dejagnu.html\">DejaGnu-Testrahmen</A>, um die Programme zu testen. Die in dieser Datei enthaltenen Definitionen gelten für alle Testfälle dieser Aufgabe. Sie werden beim Testen in die DejaGnu-Datei <TT>default.exp</TT> geschrieben. (Vergl. hierzuden Abschnitt <EM>Target dependent procedures</EM> im	<A HREF=\"http://www.gnu.org/manual/dejagnu/\" TARGET=\"_blank\">DejaGnu-Handbuch</A>.)"))

	def title(self):
		return "Tests einrichten"

	def description(self):
		return u"""Dies ist keine wirkliche Prüfung.  Sie dient nur dazu,
		den nachfolgenden Tests Definitionen zur Verfügung zu stellen.
		Diese 'Prüfung' wird immer bestanden."""

	def requires(self):
		return [ Builder ]

	# Set up tests.
	def run(self, env):
		self.setup_dirs(env)
		open(os.path.join(self.lib_dir(env), env.program() + ".exp"), 'w').close()
		default_exp = os.path.join(self.config_dir(env), "default.exp")
		fd = open(default_exp, 'w')
		defs = string.replace(self.test_defs.read(), "PROGRAM", env.program())
		fd.write(defs)
		fd.close()

		return self.result()

from praktomat.checker.admin import	CheckerInline

#from django import forms
#class SetupForm(forms.ModelForm):
#	don't show public and required, turn them off
#	class Meta:
#		model = DejaGnuTester
#		exclude = ['public', 'required'] # doesn't work
#	def clean_always(self):
#		print 'clean setup'
#		return False

class DejaGnuSetupInline(CheckerInline):
#	form = SetupForm
	model = DejaGnuSetup
	

class DejaGnuTesterInline(CheckerInline):
	model = DejaGnuTester
