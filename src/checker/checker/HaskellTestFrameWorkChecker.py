# -*- coding: utf-8 -*-

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from django.contrib import admin
from django.template.loader import get_template
from checker.basemodels import Checker, CheckerFileField, truncated_log
from checker.admin import	CheckerInline, AlwaysChangedModelForm
from solutions.models import Solution
from checker.basemodels import CheckerResult
from utilities.file_operations import *
from utilities.safeexec import execute_arglist
from utilities import encoding

from checker.compiler.HaskellBuilder import HaskellBuilder
from checker.checker.CreateFileChecker import CheckerWithFile, CopyForm

RXFAIL	   = re.compile(r"^(.*)(FAILURES!!!|your program crashed|cpu time limit exceeded|ABBRUCH DURCH ZEITUEBERSCHREITUNG|Could not find class|Killed|failures)(.*)$",	re.MULTILINE)



class IgnoringHaskellBuilder(HaskellBuilder):
	_ignore = []

	def get_file_names(self,env):
		rxarg = re.compile(self.rxarg())
		return [name for (name,content) in env.sources() if rxarg.match(name) and (not name in self._ignore)]

	def create_result(self, env):
		assert isinstance(env.solution(), Solution)
		result = CheckerResult(checker=self, solution=env.solution())
		return result

class TestOnlyBuildingBuilder(HaskellBuilder):
        _testsuite_filename = ""

	def get_file_names(self,env):
		return [self._testsuite_filename]

	def create_result(self, env):
		assert isinstance(env.solution(), Solution)
		result = CheckerResult(checker=self, solution=env.solution())
		return result

class HaskellTestFrameWorkChecker(CheckerWithFile):
	""" Checker for Haskell TestFrameWork Tests. """
	
	test_description = models.TextField(help_text = _("Description of the Testcase. To be displayed on Checker Results page when checker is unfolded."))
	name = models.CharField(max_length=100, help_text=_("Name of the Testcase. To be displayed as title on Checker Results page"))
	ignore = models.CharField(max_length=4096, help_text=_("space-seperated list of files to be ignored during compilation"),default="", blank=True)
        require_safe = models.BooleanField(default = True, help_text=_("Is a submission required to be Safe (according to GHCs Safe-Mode)?"))
        
        TESTCASE_CHOICES = ( ("DL", "Download-Link only"), ("NO", "Do not make the testcases source available"), ("FULL","Also copy the source into the report"))
        include_testcase_in_report = models.CharField(max_length=4, choices=TESTCASE_CHOICES, default = "DL", help_text=_("Make the cestcases source available via the checkers result report?"))

        _add_to_environment = False

	def title(self):
		return u"Haskell test-framework test: " + self.name

	@staticmethod
	def description():
		return u"This Checker runs a test-framework testcase existing in the sandbox. You may want to use CreateFile Checker to create test-framework .hs and possibly input data files in the sandbox."

	def output_ok(self, output):
		return (RXFAIL.search(output) == None)

        def module_name(self):
                if not self.filename.endswith(".hs"):
                        return None

                return (self.path_relative_to_sandbox().replace('/','.'))[:-3]

        def module_binary_name(self):
                if not self.filename.endswith(".hs"):
                        return None
                return (self.path_relative_to_sandbox())[:-3]

	def run(self, env):
                filecopy_result = self.run_file(env)
                if not filecopy_result.passed: return filecopy_result
                

                if self.require_safe:
                        safe_builder = IgnoringHaskellBuilder(_flags="-XSafe", _file_pattern = r"^.*\.[hH][sS]$", _main_required=False)
                        safe_builder._ignore=self.ignore.split(" ") + [self.path_relative_to_sandbox()]
                        safe_build_result = safe_builder.run(env)
                        if not safe_build_result.passed:
                                result = self.create_result(env)
                                result.set_passed(False)
                                result.set_log('<pre>' + escape(self.test_description) + '\n\n======== Test Results  (Safe) ======\n\n</pre><br/>\n'+safe_build_result.log)
                                return result

                test_builder = TestOnlyBuildingBuilder(_flags="-main-is "+self.module_name(), _libs="test-framework test-framework-quickcheck2 test-framework-hunit")
                test_builder._testsuite_filename=self.path_relative_to_sandbox()
                test_build_result = test_builder.run(env)

                if not test_build_result.passed:
                        result = self.create_result(env)
			result.set_passed(False)
			result.set_log('<pre>' + escape(self.test_description) + '\n\n======== Test Results (Building all) ======\n\n</pre><br/>\n'+test_build_result.log)
			return result

		environ = {}

		environ['UPLOAD_ROOT'] = settings.UPLOAD_ROOT

		cmd = ["./"+self.module_binary_name(), "--maximum-generated-tests=1000"]
		[output, error, exitcode,timed_out, oom_ed] = execute_arglist(cmd, env.tmpdir(),environment_variables=environ,timeout=settings.TEST_TIMEOUT,fileseeklimit=settings.TEST_MAXFILESIZE)

		result = self.create_result(env)

		(output,truncated) = truncated_log(output)
		output = '<pre>' + escape(self.test_description) + '\n\n======== Test Results ======\n\n</pre><br/><pre>' + escape(output) + '</pre>'
                
                if self.include_testcase_in_report in ["FULL","DL"]:
                        testsuit_template = get_template('checker/checker/haskell_test_framework_report.html')
                        output += testsuit_template.render({'showSource' : (self.include_testcase_in_report=="FULL"), 'testfile' : self.file, 'testfilename' : self.path_relative_to_sandbox(), 'testfileContent': encoding.get_unicode(self.file.read())})


		result.set_log(output,timed_out=timed_out or oom_ed,truncated=truncated)
		result.set_passed(not exitcode and not timed_out and not oom_ed and self.output_ok(output) and not truncated)
		return result

class HaskellTestFrameWorkCheckerInline(CheckerInline):
	""" This Class defines how the the the checker is represented as inline in the task admin page. """
	model = HaskellTestFrameWorkChecker
        form = CopyForm
