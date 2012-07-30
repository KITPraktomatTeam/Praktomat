# -*- coding: utf-8 -*-

import os, string

from django.db import models
from django.utils.translation import ugettext_lazy as _
from checker.models import Checker, CheckerResult, CheckerFileField
from utilities.file_operations import *
from utilities.encoding import *

class CreateFileChecker(Checker):
	
	file = CheckerFileField(help_text=_("The file that is copied into the sandbox"))
	filename = models.CharField(max_length=500, blank=True, help_text=_("What the file will be named in the sandbox. If empty, we try to guess the right filename!"))
	path = models.CharField(max_length=500, blank=True, help_text=_("Subfolder in the sandbox which shall contain the file."))
	
	def title(self):
		""" Returns the title for this checker category. """
		return "Copy File"
	
	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		return u"Diese Prüfung wird bestanden, falls die Zieldatei nicht schon vorhanden ist (z.B.: vom Studenten eingereicht wurde)!"
	
	def run(self, env):
		""" Runs tests in a special environment. Here's the actual work. 
		This runs the check in the environment ENV, returning a CheckerResult. """

		filename = self.filename if self.filename else self.file.path
		path = os.path.join(os.path.join(env.tmpdir(),string.lstrip(self.path,"/ ")),os.path.basename(filename))
		overridden = os.path.exists(path)
		copy_file(self.file.path, path)
		result = CheckerResult(checker=self)
		if not overridden:
			result.set_log("")
			result.set_passed(True)
		else:
			result.set_log("The file '%s' was overridden" % os.path.join(self.path, os.path.basename(self.file.path)))
			result.set_passed(False)
		source_path = os.path.join(string.lstrip(self.path,"/ "), os.path.basename(filename))
		env.add_source(source_path, get_unicode(self.file.read()))
		return result

	def show_publicly(self,passed):
		return super(CreateFileChecker,self).show_publicly(passed) or (not passed)
	
from checker.admin import	CheckerInline, AlwaysChangedModelForm

class CopyForm(AlwaysChangedModelForm):
	def __init__(self, **args):
		""" override public and required """
		super(CopyForm, self).__init__(**args)
		self.fields["public"].initial = False
		self.fields["required"].initial = False

	def clean_filename(self):
		filename = self.cleaned_data['filename']
		file = self.cleaned_data['file']
		if (not filename.strip()):
			return (os.path.basename(file.name))
		else:
			return filename
			


class CreateFileCheckerInline(CheckerInline):
	model = CreateFileChecker
	form = CopyForm

