# -*- coding: utf-8 -*-
from __future__ import unicode_literals



import os
from os.path import dirname, join
from django.conf import settings
from utilities.TestSuite import TestCase
from utilities.file_operations import copy_file, InvalidZipFile
import unittest

from solutions.models import Solution, SolutionFile
from django.core.files import File
from tasks.models import Task
from .compiler import *
from .checker import *


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
        self.solution.check_solution()

    def test_checkstyle_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'check style', 'check_ws.xml')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'check style', 'check_ws.xml')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        CheckStyleChecker.CheckStyleChecker.objects.create(
                    task = self.task,
                    order = 0,
                    configuration = dest
                    )
        self.solution.check_solution()

    def test_createfile_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'check style', 'check_ws.xml')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'check style', 'createfile.xml')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        CreateFileChecker.CreateFileChecker.objects.create(
                    task = self.task,
                    order = 0,
                    file = dest
                    )
        self.solution.check_solution()
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)

    def test_createfile_override_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'check style', 'check_ws.xml')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'check style', 'createfile.xml')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
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
        self.solution.check_solution()
        for checkerresult in self.solution.checkerresult_set.all():
            if checkerresult.checker.order == 1:
                self.assertFalse(checkerresult.passed, checkerresult.log)

    def test_createfile_zip_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'simple_zip_file.zip')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'simple_zip_file.zip')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        CreateFileChecker.CreateFileChecker.objects.create(
                    task = self.task,
                    order = 0,
                    unpack_zipfile = True,
                    file = dest
                    )
        self.solution.check_solution()
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)

    def test_createfile_illegal_zip_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'badzipfile.zip')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'badzipfile.zip')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        CreateFileChecker.CreateFileChecker.objects.create(
                    task = self.task,
                    order = 0,
                    unpack_zipfile = True,
                    file = dest
                    )
        self.assertRaises(InvalidZipFile, self.solution.check_solution)

    def test_createfile_zip_override_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'simple_zip_file.zip')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'simple_zip_file.zip')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
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
        self.solution.check_solution()
        for checkerresult in self.solution.checkerresult_set.all():
            if checkerresult.checker.order == 1:
                self.assertFalse(checkerresult.passed, checkerresult.log)



    def test_interface_checker(self):
        InterfaceChecker.InterfaceChecker.objects.create(
                    task = self.task,
                    order = 0,
                    interface1 = 'Test'
                    )
        self.solution.check_solution()
        # This fails (no good test data)
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertFalse(checkerresult.passed, checkerresult.log)

    def test_linecounter_checker(self):
        LineCounter.LineCounter.objects.create(
                    task = self.task,
                    order = 0,
                    )
        self.solution.check_solution()
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)

    def test_linewidth_checker(self):
        LineWidthChecker.LineWidthChecker.objects.create(
                    task = self.task,
                    order = 0,
                    )
        self.solution.check_solution()
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)

    def test_script_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'Power.sh')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'Power.sh')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        ScriptChecker.ScriptChecker.objects.create(
                    task = self.task,
                    order = 0,
                    shell_script = dest
                    )
        self.solution.check_solution()
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)

    def test_script_timeout(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'loop.sh')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'loop.sh')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        with self.settings(TEST_TIMEOUT=1):
            ScriptChecker.ScriptChecker.objects.create(
                task = self.task,
                order = 0,
                shell_script = dest
            )
            self.solution.check_solution()
            for checkerresult in self.solution.checkerresult_set.all():
                self.assertIn('1', checkerresult.log, "Test did not even start?")
                self.assertIn('Timeout occurred!', checkerresult.log, "Test result does not mention timeout")
                # (string 'Timeout occurred!' defined in checker/basemodels.py : CheckerResult.set_log)
                self.assertFalse(checkerresult.passed, "Test succeed (no timeout?)")
                self.assertNotIn('done', checkerresult.log, "Test did finish (no timeout?)")


    @unittest.skipIf('TRAVIS' in os.environ, "ulimit doesn’t seem to work on travis")
    @unittest.skipIf(settings.USESAFEDOCKER, "not yet supported with safe-docker")
    def test_script_filesizelimit(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'largefile.pl')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'largefile.pl')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        with self.settings(TEST_MAXFILESIZE=5):
            ScriptChecker.ScriptChecker.objects.create(
                task = self.task,
                order = 0,
                shell_script = dest
                )
            self.solution.check_solution()
            for checkerresult in self.solution.checkerresult_set.all():
                self.assertIn('Begin', checkerresult.log, "Test did not even start? (%s)" % checkerresult.log)
                self.assertNotIn('End', checkerresult.log, "Test did finish (no timeout?) (%s)" % checkerresult.log)
                #self.assertIn('Timeout occurred!', checkerresult.log, "Test result does not mention timeout")
                # (string 'Timeout occurred!' defined in checker/basemodels.py : CheckerResult.set_log)
                self.assertFalse(checkerresult.passed, "Test succeed (no timeout?)")


    @unittest.skipIf(not settings.USESAFEDOCKER, "only supported with safe-docker")
    def test_script_memorylimit(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'allocate.pl')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'allocate.pl')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        with self.settings(TEST_MAXMEM=1):
            ScriptChecker.ScriptChecker.objects.create(
                task = self.task,
                order = 0,
                shell_script = dest
                )
            self.solution.check_solution()
            for checkerresult in self.solution.checkerresult_set.all():
                self.assertIn('Begin', checkerresult.log, "Test did not even start?")
                self.assertNotIn('End', checkerresult.log, "Test did finish (no timeout?)")
                self.assertIn('Timeout occurred!', checkerresult.log, "Test result does not mention timeout")
                # (string 'Timeout occurred!' defined in checker/basemodels.py : CheckerResult.set_log)
                self.assertFalse(checkerresult.passed, "Test succeed (no timeout?)")

    def test_text_checker(self):
        TextChecker.TextChecker.objects.create(
                    task = self.task,
                    order = 0,
                    text = 'System.out'
                    )
        self.solution.check_solution()
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)

    def test_dejagnu_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'GGT', 'solutions', 'javagently', 'Stream.java')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit',  'javagently', 'Stream.java')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        CreateFileChecker.CreateFileChecker.objects.create(
                    task = self.task,
                    order = 0,
                    file = dest,
                    path = "javagently"
                    )
        JavaBuilder.JavaBuilder.objects.create(
                    task = self.task,
                    order = 1,
                    _flags = "",
                    _output_flags = "",
                    _file_pattern = r"^[a-zA-Z0-9_/\\]*\.[jJ][aA][vV][aA]$"
                    )
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'GGT', 'DejaGnuTestCases', 'default.exp')
        test_defs = join(settings.UPLOAD_ROOT, 'directdeposit', 'DejaGnuTestCases', 'default.exp')
        # circumvent SuspiciousOperation exception
        copy_file(src, test_defs)
        DejaGnu.DejaGnuSetup.objects.create(
                    task = self.task,
                    order = 1,
                    test_defs = test_defs
                    )
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'Tasks', 'GGT', 'DejaGnuTestCases', 'public.exp')
        test_case = join(settings.UPLOAD_ROOT, 'directdeposit', 'DejaGnuTestCases', 'public.exp')
        # circumvent SuspiciousOperation exception
        copy_file(src, test_case)
        DejaGnu.DejaGnuTester.objects.create(
                    task = self.task,
                    order = 2,
                    test_case = test_case
                    )

        self.solution.check_solution()

        # Check if they are all finished, or if one of the dependencies failed.
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)

    def test_c_checker(self):
        src = join(dirname(dirname(dirname(__file__))), 'examples', 'Hello World.c')
        dest = join(settings.UPLOAD_ROOT, 'directdeposit', 'Hello World.c')
        # circumvent SuspiciousOperation exception
        copy_file(src, dest)
        CreateFileChecker.CreateFileChecker.objects.create(
                    task = self.task,
                    order = 0,
                    file = dest,
                    )
        CBuilder.CBuilder.objects.create(
                    task = self.task,
                    order = 1,
                    _file_pattern = r"^[a-zA-Z0-9_ ]*\.[cC]$"
                    )
        self.solution.check_solution()

        # Check if they are all finished, or if one of the dependencies failed.
        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)

    def test_r_checker(self):
        import mimetypes
        mimetypes.init()
        self.assertTrue(mimetypes.inited)
        # TODO: This is duplicated from solutions/forms.py. Where should this go?
        for (mimetype, extension) in settings.MIMETYPE_ADDITIONAL_EXTENSIONS:
            mimetypes.add_type(mimetype, extension, strict=True)
        solution_file = SolutionFile(solution = self.solution)
        solution_file.mime_type=mimetypes.guess_type('example.R')[0]
        # Bughunting for Python 3.9.12 and above
        # at time of bughunting ... uses pysqlite 2.6.0 with SQLite 3.38.3
        # see https://github.com/KITPraktomatTeam/Praktomat/issues/336
        #
        # Unit Tests for R Checker fail : missing mimetype for example.R
        # django.db.utils.IntegrityError: NOT NULL constraint failed: solutions_solutionfile.mime_type
        self.assertEqual(str(mimetypes.types_map['.R']),solution_file.mime_type, "Mimetype for extension R should be guessed right")
        self.assertIsNotNone(solution_file.mime_type, "Mimetype for example.R shouldn't be None")
        with open(join(dirname(dirname(dirname(__file__))), 'examples', 'example.R',)) as fd:
            solution_file.file.save('example.R', File(fd))

        RChecker.RChecker.objects.create(
            task = self.task,
            order = 0,
            )

        self.solution.check_solution()

        try:
            for checkerresult in self.solution.checkerresult_set.all():
                self.assertIn('2', checkerresult.log, "Test did not calculate 1 + 2 (%s)" % checkerresult.log)
                self.assertTrue(checkerresult.passed, checkerresult.log)
                self.assertTrue(checkerresult.artefacts.exists())
                self.assertEqual(checkerresult.artefacts.get().path(), "Rplots.pdf")
        finally:
            solution_file.delete()

    def test_r_checker_2(self):
        import mimetypes
        mimetypes.init()
        # TODO: This is duplicated from solutions/forms.py. Where should this go?
        for (mimetype, extension) in settings.MIMETYPE_ADDITIONAL_EXTENSIONS:
            mimetypes.add_type(mimetype, extension, strict=True)
        solution_file = SolutionFile(solution = self.solution)
        solution_file.mime_type=mimetypes.guess_type('example.R')[0]
        # Bughunting for Python 3.9.12 and above
        # at time of bughunting ... uses pysqlite 2.6.0 with SQLite 3.38.3
        # see https://github.com/KITPraktomatTeam/Praktomat/issues/336
        #
        # Unit Tests for R Checker fail : missing mimetype for example.R
        # django.db.utils.IntegrityError: NOT NULL constraint failed: solutions_solutionfile.mime_type
        self.assertIsNotNone(solution_file.mime_type, "Mimetype for example.R shouldn't be None")
        with open(join(dirname(dirname(dirname(__file__))), 'examples', 'example.R',)) as fd:
            solution_file.file.save('example.R', File(fd))

        RChecker.RChecker.objects.create(
            task = self.task,
            order = 0,
            r_script = 'example.R',
            )

        self.solution.check_solution()

        try:
            for checkerresult in self.solution.checkerresult_set.all():
                self.assertIn('2', checkerresult.log, "Test did not calculate 1 + 2 (%s)" % checkerresult.log)
                self.assertTrue(checkerresult.passed, checkerresult.log)
                self.assertTrue(checkerresult.artefacts.exists())
                self.assertEqual(checkerresult.artefacts.get().path(), "Rplots.pdf")
        finally:
                solution_file.delete()

    def test_r_checker_3(self):
        import mimetypes
        mimetypes.init()
        # TODO: This is duplicated from solutions/forms.py. Where should this go?
        for (mimetype, extension) in settings.MIMETYPE_ADDITIONAL_EXTENSIONS:
            mimetypes.add_type(mimetype, extension, strict=True)
        solution_file = SolutionFile(solution = self.solution)
        solution_file.mime_type=mimetypes.guess_type('example.R')[0]
        # Bughunting for Python 3.9.12 and above
        # at time of bughunting ... uses pysqlite 2.6.0 with SQLite 3.38.3
        # see https://github.com/KITPraktomatTeam/Praktomat/issues/336
        #
        # Unit Tests for R Checker fail : missing mimetype for example.R
        # django.db.utils.IntegrityError: NOT NULL constraint failed: solutions_solutionfile.mime_type
        self.assertIsNotNone(solution_file.mime_type, "Mimetype for example.R shouldn't be None")
        with open(join(dirname(dirname(dirname(__file__))), 'examples', 'example.R',)) as fd:
            solution_file.file.save('example.R', File(fd))

        RChecker.RChecker.objects.create(
            task = self.task,
            order = 0,
            r_script = 'not-example.R',
            )

        self.solution.check_solution()

        try:
            for checkerresult in self.solution.checkerresult_set.all():
                self.assertIn('Could not find expected R script', checkerresult.log, "Test did not complain (%s)" % checkerresult.log)
                self.assertFalse(checkerresult.passed, checkerresult.log)
        finally:
            solution_file.delete()

    def test_r_checker_4(self):
        import mimetypes
        mimetypes.init()
        # TODO: This is duplicated from solutions/forms.py. Where should this go?
        for (mimetype, extension) in settings.MIMETYPE_ADDITIONAL_EXTENSIONS:
            mimetypes.add_type(mimetype, extension, strict=True)
        solution_file = SolutionFile(solution = self.solution)
        solution_file.mime_type=mimetypes.guess_type('example.R')[0]
        # Bughunting for Python 3.9.12 and above
        # at time of bughunting ... uses pysqlite 2.6.0 with SQLite 3.38.3
        # see https://github.com/KITPraktomatTeam/Praktomat/issues/336
        #
        # Unit Tests for R Checker fail : missing mimetype for example.R
        # django.db.utils.IntegrityError: NOT NULL constraint failed: solutions_solutionfile.mime_type
        #
        # at one place let show the uncatched problem
        # self.assertIsNotNone(solution_file.mime_type, "Mimetype for example.R shouldn't be None")
        with open(join(dirname(dirname(dirname(__file__))), 'examples', 'example.R',)) as fd:
            solution_file.file.save('example.R', File(fd))

        solution_file2 = SolutionFile(solution = self.solution)
        solution_file2.mime_type=mimetypes.guess_type('example2.R')[0]
        with open(join(dirname(dirname(dirname(__file__))), 'examples', 'example.R',)) as fd:
            solution_file2.file.save('example2.R', File(fd))

        RChecker.RChecker.objects.create(
            task = self.task,
            order = 0,
            )

        self.solution.check_solution()

        try:
            for checkerresult in self.solution.checkerresult_set.all():
                self.assertIn('Multiple R scripts found', checkerresult.log, "Test did not complain (%s)" % checkerresult.log)
                self.assertFalse(checkerresult.passed, checkerresult.log)
        finally:
            solution_file.delete()
            solution_file2.delete()

    def test_keep_file_checker(self):
        KeepFileChecker.KeepFileChecker.objects.create(
            task = self.task,
            order = 0,
            filename = "GgT.java",
            )

        self.solution.check_solution()

        for checkerresult in self.solution.checkerresult_set.all():
            self.assertTrue(checkerresult.passed, checkerresult.log)
            self.assertTrue(checkerresult.artefacts.exists())
            self.assertEqual(checkerresult.artefacts.get().path(), "GgT.java")

    def test_keep_file_checker_2(self):
        KeepFileChecker.KeepFileChecker.objects.create(
            task = self.task,
            order = 0,
            filename = "does-not-exist",
            )

        self.solution.check_solution()

        for checkerresult in self.solution.checkerresult_set.all():
            self.assertIn('Could not find file', checkerresult.log, "Test did not complain (%s)" % checkerresult.log)
            self.assertFalse(checkerresult.passed, checkerresult.log)
