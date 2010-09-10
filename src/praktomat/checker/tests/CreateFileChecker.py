# -*- coding: utf-8 -*-

import shutil, os

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from praktomat.checker.models import Checker, CheckerResult

class CreateFileChecker(Checker):
	
	upload_dir = "AdminFiles/CopyChecker/%Y%m%d%H%M%S/"
	file = models.FileField(storage=settings.STORAGE, upload_to=upload_dir, help_text=_("The file that is copied into the temporary test directory"))
	path = models.CharField(max_length=500, blank=True, help_text=_("Subfolder in the sandbox which shall contain the file."))
	
	def title(self):
		""" Returns the title for this checker category. """
		return "Copy File"
	
	def description(self):
		""" Returns a description for this Checker. """
		return u"""Diese Prüfung wird immer bestanden."""
	
	def run(self, env):
		""" Runs tests in a special environment. Here's the actual work. 
		This runs the check in the environment ENV, returning a CheckerResult. """
		absolute_path = os.path.join(env.tmpdir(), self.path)
		if self.path:
			os.mkdir(absolute_path)
		shutil.copy(self.file.path, absolute_path)
		result = CheckerResult(checker=self)
		result.set_log("")
		result.set_passed(True)
		return result
	
from praktomat.checker.admin import	CheckerInline
from django import forms

class CopyForm(forms.ModelForm):
	def __init__(self, **args):
		""" override public and required """
		super(CopyForm, self).__init__(**args)
		self.fields["public"].initial = False
		self.fields["required"].initial = False

class CreateFileCheckerInline(CheckerInline):
	model = CreateFileChecker
	form = CopyForm

