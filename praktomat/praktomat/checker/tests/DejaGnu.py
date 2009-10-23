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

#import Checker
#import CheckerFactory
#import Builder
#import configured
#import this
#import Net

#from misc import *

# Stuff to highlight in output
RXFAIL	   = re.compile(r"^(.*)(FAIL|ERROR|Abort|Exception |your program crashed|cpu time limit exceeded|"
						"ABBRUCH DURCH ZEITUEBERSCHREITUNG|# of unexpected failures.*[0-9]+)(.*)$",	re.MULTILINE)
RXPASS	   = re.compile(r"^(.*)(PASS)(.*)$", re.MULTILINE)
RXRUN_BY   = re.compile(r"Run By .* on ")

# Stuff to remove from output
RXREMOVE   = re.compile(r"(Schedule of variations:.*interface file.)|(Running \./[ -z]*/[a-z]*\.exp \.\.\.)", re.DOTALL)

# Maximal size of test output read
MAX_OUTPUT = 1000000

from django.core.files.storage import FileSystemStorage
file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
# Write out a file to be used as default content
#file_storage.save('tests/default.txt', ContentFile('default content'))


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
#	def __init__(self):
#		Checker.Checker.__init__(self)
#		self._test_cases = DEFAULT_TEST_CASES
	
	
	
	#def _get_upload_path(instance, filename):
	#	return "DejaGnuTestCases/Task" + instance.task().id + "/%d" + filename
	test_case = models.FileField(upload_to="upload/admin/DejaGnuTestCases/%Y%m%d%H%M%S/",default='DejaGnuDefaultTest.exp') # Needs real default!

	def __unicode__(self):
		return "DejaGnu Test"
	
	def title(self):
		return "Tests"
		
	def description(self):
		return u"Diese Prüfung ist bestanden, wenn alle Testfälle zum erwarteten Ergebnis führten."

	def default_title(self): # hmmmmmm
		if self.public():
			if self.required():
				return self.title()
			else:
				return self.title() + " (ergänzend)"
		else:
			return self.title() + " (geheim)"

	
#	def set_test_cases(self, test_cases):
#		# assert(isinstance(test_cases, str))
#		self.test_cases = test_cases
#
#	def test_cases(self):
#		return self.test_cases



#	def print_body(self, page, checker_id):
#		print """In den folgenden DejaGnu-Testf&auml;llen werden
#		typischerweise Funktionen aufgerufen, die beim vorherigen
#		Schritt <EM>Tests einrichten</EM> definiert wurden.	 Siehe
#		auch den Abschnitt <EM>How to write a test case</EM> im <A
#		TARGET="_blank"
#		HREF="http://www.gnu.org/manual/dejagnu/">DejaGnu-Handbuch</A>.
#		<P> Auch dieser Text wird mit M4 bearbeitet.  Die Zeichenkette
#		`<TT>PROGRAM</TT>' wird durch den vom Benutzer angegebenen
#		Programmnamen ersetzt."""
#
#		page.print_textarea(checker_id + ".test_cases", self.test_cases())
#
#		print "Als Datei"
#		task = page.task()
#		if task != None:
#			print page.link_data('DownloadTestCasesPage', "herunterladen",
#								 { "checker_id": checker_id },
#								 "tests.exp")
#		else:
#			print "<S>herunterladen</S>"
#
#		if page.editing():
#			print "| heraufladen:"
#			page.print_file(checker_id + ".test_cases_upload")
#		
#		Checker.Checker.print_body(self, page, checker_id)
#
#	def update(self, form, checker_id):
#		upload_id = checker_id + ".test_cases_upload"
#		if (form.has_key(upload_id) and form[upload_id].filename):
#			self.set_test_cases(string.strip(form[upload_id].value))
#		else:
#			text_id = checker_id + ".test_cases"
#			self.set_test_cases(string.strip(form[text_id].value))
#
#		Checker.Checker.update(self, form, checker_id)

	def requires(self):
		return [ DejaGnuSetup ]

	# Return 1 if the output is ok
	def output_ok(self, output):
		return (RXFAIL.search(output) == None and
				string.find(output, "runtest completed") >= 0 and 
				string.find(output, "non-expected failures") < 0 and
				string.find(output, "unexpected failures") < 0)

	#
	# Runs a test.
	#
	# Returns a CheckerResult.
	#
	# def runtest(self, testsuite, user_name, program_name, test_case, timeout=None):
	# quick hack sets default timeout to 120 seconds
	#def runtest(self, testsuite, user_name, program_name, test_case, timeout=120):
#		cmd = "USER=" + sh_quote(user_name) + "; export USER; " + \
#			  "HOME=" + testsuite + "; export HOME; " + \
#			  "cd " + testsuite + "; " + \
#			  RUNTEST + " --tool " + program_name + \
#			  " " + test_case + " 2>&1"
#		
#		if timeout is None:
#			res = Net.read_all(cmd)
#		else:
#			res = Net.read_all(cmd, timeout)
#
#		output=res[0]
#		try:
#			summary = open(os.path.join(testsuite,
#										program_name + ".sum")).read()
#			log		= open(os.path.join(testsuite,
#										program_name + ".log")).read()
#		except:
#			summary = ""
#			log		= ""
#
#		complete_output = output + log
#
#		result = self.result()
#		if res[1]:
#			complete_output = complete_output + "ERROR: Ein TimeOut ist aufgetreten!"
#		result.set_log(complete_output)
#		result.set_passed((not res[1]) & self.output_ok(complete_output))
#		
#		return result

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

		# Run the tests
		#return self.runtest(self.testsuite_dir(env), env.user().realname(),
		#					env.program(), "tests.exp")
		#runtest(self, testsuite, user_name, program_name, test_case, timeout=120):
							
		#cmd = "USER=" + sh_quote(user_name) + "; export USER; " + \
		#	  "HOME=" + testsuite + "; export HOME; " + \
		#	  "cd " + testsuite + "; " + \
		#	  RUNTEST + " --tool " + program_name + \
		#	  " " + test_case + " 2>&1"
		
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
			complete_output += "ERROR: Ein TimeOut ist aufgetreten!" # Or propably somsing else happend? 
		
		result = self.result()
		result.set_log(self.htmlize_output(complete_output))
		result.set_passed((not error) & self.output_ok(complete_output))
		#assert False
		return result

# A template for test cases.
DEFAULT_TEST_CASES = """# `tests.exp' template
# Insert test cases in the format
# PROGRAM_test "[input]" "[expected_output]"
"""






# Global definitions for test cases.
class DejaGnuSetup(Checker, DejaGnu):
#	def __init__(self, *kwargs):
#		Checker.__init__(self, *kwargs)
#		from praktomat.checker.tests.DejaGnuDefaultDefs import DEFAULT_TEST_DEFS
#		self._test_defs = DEFAULT_TEST_DEFS		# Test definitions

	test_defs = models.FileField(upload_to="upload/admin/DejaGnuTestCases/%Y%m%d%H%M%S/")
	
	def title(self):
		return "Tests einrichten"

	def description(self):
		return u"""Dies ist keine wirkliche Prüfung.  Sie dient nur dazu,
		den nachfolgenden Tests Definitionen zur Verfügung zu stellen.
		Diese 'Prüfung' wird immer bestanden."""

#	def print_body(self, page, checker_id):
#		print this.NAME + """ benutzt den <A
#HREF="http://www.gnu.org/software/dejagnu/dejagnu.html">DejaGnu-Testrahmen</A>,
#		um die Programme zu testen.
#		<P>
#		Diese folgenden Definitionen gelten f&uuml;r alle Testf&auml;lle
#		dieser Aufgabe.	 Sie werden beim Testen in die DejaGnu-Datei
#		<TT>default.exp</TT> geschrieben.  (Vergl. hierzu
#		den Abschnitt <EM>Target dependent procedures</EM> im
#		<A HREF="http://www.gnu.org/manual/dejagnu/"
#		TARGET="_blank">DejaGnu-Handbuch</A>.)
#		<P>
#		Auch dieser Text wird mit M4 bearbeitet.  Die Zeichenkette
#		`<TT>PROGRAM</TT>' wird durch den vom Benutzer angegebenen
#		Programmnamen ersetzt.
#		"""
#
#		page.print_textarea(checker_id + ".test_defs", self.test_defs())
#
#		print "Als Datei"
#		print page.link_data('DownloadTestDefsPage', "herunterladen",
#							 { "checker_id": checker_id },
#							 "default.exp")
#
#		if page.editing():
#			print "| heraufladen:"
#			page.print_file(checker_id + ".test_defs_upload")
#
#		Checker.Checker.print_body(self, page, checker_id)
#
#	def update(self, form, checker_id):
#		upload_id = checker_id + ".test_defs_upload"
#		if (form.has_key(upload_id) and form[upload_id].filename):
#			self.set_test_defs(string.strip(form[upload_id].value))
#		else:
#			text_id = checker_id + ".test_defs"
#			self.set_test_defs(string.strip(form[text_id].value))
#
#		Checker.Checker.update(self, form, checker_id)

	def requires(self):
		return [ Builder ]

	# Setting up the tests is always secret; passing is not required.
	def public(self): # UHHHHOHHHH
		return 0
	def required(self):
		return 0

#	def set_test_defs(self, test_defs):
#		assert(isinstance(test_defs, str))
#		self._test_defs = test_defs
#
#	def test_defs(self):
#		return self.test_defs.read()

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

class DejaGnuSetupInline(CheckerInline):
	model = DejaGnuSetup

class DejaGnuTesterInline(CheckerInline):
	model = DejaGnuTester
