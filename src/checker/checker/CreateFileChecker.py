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
import zipfile


class CheckerWithFile(Checker):
       	class Meta:
		abstract = True
        
	file = CheckerFileField(help_text=_("The file that is copied into the sandbox"))
	filename = models.CharField(max_length=500, blank=True, help_text=_("What the file will be named in the sandbox. If empty, we try to guess the right filename!"))
	path = models.CharField(max_length=500, blank=True, help_text=_("Subfolder in the sandbox which shall contain the file."))
        unpack_zipfile = models.BooleanField(default=False, help_text=_("Unpack the zip file into the given subfolder. (It will be an error if the file is not a zip file; the filename is ignored.)")) 

        _add_to_environment = True

        def path_relative_to_sandbox(self):
		filename = self.filename if self.filename else self.file.path
                return os.path.join(string.lstrip(self.path,"/ "), os.path.basename(filename))
	
	def run_file(self, env):
		result = CheckerResult(checker=self)
		clashes = []
		if (self.unpack_zipfile):
			lpath = string.lstrip(self.path,"/ ")
			path = os.path.join(env.tmpdir(),lpath)
			if not zipfile.is_zipfile(self.file.path):
				raise ValidationError("File %s is not a zipfile." % self.file.path)
			zip = zipfile.ZipFile(self.file.path, 'r')
			
			if zip.testzip():
				raise ValidationError("File %s is invalid." % self.file.path)
			# zip.extractall would not protect against ..-paths,
			# it would do so from python 2.7.4 on.
			for finfo in zip.infolist():
				dest = os.path.join(path, finfo.filename)
				# This check is from http://stackoverflow.com/a/10077309/946226
				if not os.path.realpath(os.path.abspath(dest)).startswith(path):
					raise ValidationError("File %s contains illegal path %s." % (self.file.path, finfo.filename))
				if os.path.exists(dest):
					clashes.append(os.path.join(lpath, finfo.filename))
				zip.extract(finfo, path)
		else:
			filename = self.filename if self.filename else self.file.path
			path = os.path.join(os.path.join(env.tmpdir(),string.lstrip(self.path,"/ ")),os.path.basename(filename))
			overridden = os.path.exists(path)
			copy_file(self.file.path, path, binary=True)
			if overridden:
				clashes.append(os.path.join(self.path, os.path.basename(filename)))
			source_path = os.path.join(string.lstrip(self.path,"/ "), os.path.basename(filename))
			if (self._add_to_environment):
				env.add_source(source_path, self.file.read())

		result.set_passed(not clashes)
		if clashes:
			result.set_log("These files already existed. Do NOT include them in your submissions:<br/><ul>\n" + "\n".join(map(lambda f: "<li>%s</li>" % escape(f), clashes)) + "</ul>")
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
		self.fields["required"].initial = True

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

