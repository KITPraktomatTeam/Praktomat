from os.path import dirname, join
from django.conf import settings
from utilities.TestSuite import TestCase
from utilities.file_operations import copy_file, InvalidZipFile

from solutions.models import Solution
from tasks.models import Task
from compiler import *
from checker import *


class TestChecker(TestCase):
	def setUp(self):
		self.solution = Solution.objects.all()[0]
		self.task = self.solution.task

	def tearDown(self):
		pass
		
	def test_anonymity_checker(self):
		AnonymityChecker.AnonymityChecker.objects.create(
				task = self.task,
				order = 0
				)
		self.solution.check()

	def test_checkstyle_checker(self):
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'check style', 'check_ws.xml')	
		dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'check style', 'check_ws.xml')
		# circumvent SuspiciousOperation exception
		copy_file(src,dest)
		CheckStyleChecker.CheckStyleChecker.objects.create(
					task = self.task,
					order = 0,
					configuration = dest
					)
		self.solution.check()

	def test_createfile_checker(self):
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'check style', 'check_ws.xml')	
		dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'check style', 'createfile.xml')
		# circumvent SuspiciousOperation exception
		copy_file(src,dest)
		CreateFileChecker.CreateFileChecker.objects.create(
					task = self.task,
					order = 0,
					file = dest
					)
		self.solution.check()
		for checkerresult in self.solution.checkerresult_set.all():
			self.failUnless(checkerresult.passed, checkerresult.log)

	def test_createfile_override_checker(self):
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'check style', 'check_ws.xml')	
		dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'check style', 'createfile.xml')
		# circumvent SuspiciousOperation exception
		copy_file(src,dest)
		CreateFileChecker.CreateFileChecker.objects.create(
					task = self.task,
					order = 0,
					file = dest
					)
		CreateFileChecker.CreateFileChecker.objects.create(
					task = self.task,
					order = 1,
					file = dest
					)
		self.solution.check()
		for checkerresult in self.solution.checkerresult_set.all():
                        if checkerresult.checker.order == 1:
                            self.failIf(checkerresult.passed, checkerresult.log)

	def test_createfile_zip_checker(self):
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'simple_zip_file.zip')
		dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'simple_zip_file.zip')
		# circumvent SuspiciousOperation exception
		copy_file(src,dest, binary=True)
		CreateFileChecker.CreateFileChecker.objects.create(
					task = self.task,
					order = 0,
                                        unpack_zipfile = True,
					file = dest
					)
		self.solution.check()
		for checkerresult in self.solution.checkerresult_set.all():
			self.failUnless(checkerresult.passed, checkerresult.log)

	def test_createfile_illegal_zip_checker(self):
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'badzipfile.zip')
		dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'badzipfile.zip')
		# circumvent SuspiciousOperation exception
		copy_file(src,dest, binary=True)
		CreateFileChecker.CreateFileChecker.objects.create(
					task = self.task,
					order = 0,
                                        unpack_zipfile = True,
					file = dest
					)
                self.assertRaises(InvalidZipFile, self.solution.check)

	def test_createfile_zip_override_checker(self):
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'simple_zip_file.zip')
		dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'simple_zip_file.zip')
		# circumvent SuspiciousOperation exception
		copy_file(src,dest, binary=True)
		CreateFileChecker.CreateFileChecker.objects.create(
					task = self.task,
					order = 0,
                                        unpack_zipfile = True,
					file = dest
					)
		CreateFileChecker.CreateFileChecker.objects.create(
					task = self.task,
					order = 1,
                                        unpack_zipfile = True,
					file = dest
					)
		self.solution.check()
		for checkerresult in self.solution.checkerresult_set.all():
                        if checkerresult.checker.order == 1:
                            self.failIf(checkerresult.passed, checkerresult.log)



	def test_interface_checker(self):
		InterfaceChecker.InterfaceChecker.objects.create(
					task = self.task,
					order = 0,
					interface1 = 'Test'
					)
		self.solution.check()
                # This fails (no good test data)
		for checkerresult in self.solution.checkerresult_set.all():
			self.failIf(checkerresult.passed, checkerresult.log)

	def test_linecounter_checker(self):
		LineCounter.LineCounter.objects.create(
					task = self.task,
					order = 0,
					)
		self.solution.check()
		for checkerresult in self.solution.checkerresult_set.all():
			self.failUnless(checkerresult.passed, checkerresult.log)

	def test_linewidth_checker(self):
		LineWidthChecker.LineWidthChecker.objects.create(
					task = self.task,
					order = 0,
					)
		self.solution.check()
		for checkerresult in self.solution.checkerresult_set.all():
			self.failUnless(checkerresult.passed, checkerresult.log)

	def test_script_checker(self):
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'Power.sh')	
		dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'Power.sh')
		# circumvent SuspiciousOperation exception
		copy_file(src,dest)
		ScriptChecker.ScriptChecker.objects.create(
					task = self.task,
					order = 0,
					shell_script = dest
					)
		self.solution.check()
		for checkerresult in self.solution.checkerresult_set.all():
			self.failUnless(checkerresult.passed, checkerresult.log)

	def test_text_checker(self):
		TextChecker.TextChecker.objects.create(
					task = self.task,
					order = 0,
					text = 'System.out'
					)
		self.solution.check()
		for checkerresult in self.solution.checkerresult_set.all():
			self.failUnless(checkerresult.passed, checkerresult.log)

	def test_dejagnu_checker(self):
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'GGT', 'solutions', 'javagently', 'Stream.java')	
		dest = join(settings.UPLOAD_ROOT, 'directdeposit',  'javagently', 'Stream.java')
		# circumvent SuspiciousOperation exception
		copy_file(src,dest)
		CreateFileChecker.CreateFileChecker.objects.create(
					task = self.task,
					order = 0,
					file = dest,
					path = "javagently"
					)
		JavaBuilder.JavaBuilder.objects.create(
					task = self.task,
					order = 0,
					_flags = "",
					_output_flags = "",
					_file_pattern = r"^[a-zA-Z0-9_/\\]*\.[jJ][aA][vV][aA]$"
					)
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'GGT', 'DejaGnuTestCases', 'default.exp')	
		test_defs = join(settings.UPLOAD_ROOT, 'directdeposit', 'DejaGnuTestCases', 'default.exp')
		# circumvent SuspiciousOperation exception
		copy_file(src,test_defs)
		DejaGnu.DejaGnuSetup.objects.create(
					task = self.task,
					order = 1,
					test_defs = test_defs
					)
		src = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'GGT', 'DejaGnuTestCases', 'public.exp')
		test_case = join(settings.UPLOAD_ROOT, 'directdeposit', 'DejaGnuTestCases', 'public.exp')
		# circumvent SuspiciousOperation exception
		copy_file(src,test_case)
		DejaGnu.DejaGnuTester.objects.create(
					task = self.task,
					order = 2,
					test_case = test_case
					)

		self.solution.check()

		# Check if they are all finished, or if one of the dependencies failed.
		for checkerresult in self.solution.checkerresult_set.all():
			self.failUnless(checkerresult.passed, checkerresult.log)
			

