# -*- coding: utf-8 -*-

import os, string

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from checker.models import Checker, CheckerResult, CheckerFileField
from utilities.file_operations import *
from utilities.encoding import *
from django.utils.html import escape
from django.contrib import admin



class CheckerWithFile(Checker):
       	class Meta:
		abstract = True
        
	file = CheckerFileField(help_text=_("The file that is copied into the sandbox"))
	filename = models.CharField(max_length=500, blank=True, help_text=_("What the file will be named in the sandbox. If empty, we try to guess the right filename!"))
	path = models.CharField(max_length=500, blank=True, help_text=_("Subfolder in the sandbox which shall contain the file."))

        _add_to_environment = True

        def path_relative_to_sandbox(self):
		filename = self.filename if self.filename else self.file.path
                return os.path.join(string.lstrip(self.path,"/ "), os.path.basename(filename))

	def run_file(self, env):
		filename = self.filename if self.filename else self.file.path
		path = os.path.join(os.path.join(env.tmpdir(),string.lstrip(self.path,"/ ")),os.path.basename(filename))
		overridden = os.path.exists(path)
		copy_file_to_directory_verbatim(self.file.path, path,to_is_directory=False)
		result = CheckerResult(checker=self)
		if not overridden:
			result.set_log("")
			result.set_passed(True)
		else:
			result.set_log("The file '%s' already exists. Do NOT include it in your submission!" % escape(os.path.join(self.path, os.path.basename(filename))))
			result.set_passed(False)
		source_path = os.path.join(string.lstrip(self.path,"/ "), os.path.basename(filename))
		if (self._add_to_environment):
                        env.add_source(source_path, self.file.read())
		return result

class CreateFileChecker(CheckerWithFile):
	
	def title(self):
		""" Returns the title for this checker category. """
		return "Copy File"
	
	@staticmethod
	def description():
		""" Returns a description for this Checker. """
		return u"Diese Prüfung wird bestanden, falls die Zieldatei nicht schon vorhanden ist (z.B.: vom Studenten eingereicht wurde)!"
	
	def run(self, env):
                return self.run_file(env)


	def show_publicly(self,passed):
		return super(CreateFileChecker,self).show_publicly(passed) or (not passed)

	def clean(self):
		super(CreateFileChecker, self).clean()
		if not (self.required and self.always and (not self.public)): raise ValidationError("Florian says: CreateFileCheckers have to be required, always, non-public")
 
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

