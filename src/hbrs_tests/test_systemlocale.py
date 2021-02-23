# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

import sys
import locale
import os


class SystemLocaleTest(TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_systemlocale_printout(self):
        print("")
        print("sys:defaultencoding: " , sys.getdefaultencoding())
        print("sys:filesystemencoding: " ,sys.getfilesystemencoding())
        print("locale:preferredencoding: " , locale.getpreferredencoding())
        print("locale:defaultlocale: ",locale.getdefaultlocale())
        print("locale:locale: ",locale.getlocale())
        print("OS LANG: ", os.getenv("LANG"))
        print("OS LANGUAGE: ", os.getenv("LANGUAGE"))
        print("")
        self.assertTrue(True)

    def test_filesystemencoding_is_utf8(self):
        self.assertEqual(sys.getfilesystemencoding().upper(), 'UTF-8')

    def test_preferredencoding_is_UTF8(self):
        self.assertEqual(locale.getpreferredencoding().upper(), 'UTF-8')

    def test_encoding_of_defaultlocale_is_UTF8(self):
        self.assertTrue(locale.getdefaultlocale()[1] is not None , msg="Python could not determine a default locale.")
        self.assertEqual(locale.getdefaultlocale()[1].upper(), 'UTF-8')

    def test_encoding_of_locale_is_UTF8(self):
        self.assertEqual(locale.getlocale()[1].upper(), 'UTF-8')

    def test_LANG_environmentvariable_as_UTF8(self):
        os_lang=os.getenv("LANG")
        self.assertTrue(os_lang is not None , msg="OS environment variable LANG is not defined. It have to define UTF-8")
        self.assertNotEqual(os_lang, "", msg="OS environment variable LANG has no value.")
        self.assertTrue('UTF-8' in os_lang.upper(), msg="OS environment variable LANG is not defining UTF-8: it is \"%s\" " % os_lang )

    def test_LANGUAGE_environmentvariable_is_not_None(self):
        os_language=os.getenv("LANGUAGE")
        self.assertTrue(os_language is not None , msg="OS environment variable LANGUAGE is not defined.")
        self.assertNotEqual(os_language, "", msg="OS environment variable LANGUAGE has no value.")
