# -*- coding: utf-8 -*-

import os.path
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from checker.models import Checker, CheckerResult, CheckerResultArtefact, CheckerFileField
from utilities.file_operations import *
from utilities.encoding import *
from django.utils.html import escape
from django.contrib import admin
from django.core.files import File


class KeepFileChecker(Checker):
	filename = models.CharField(max_length=500, blank=True, help_text=_("The name of the file to preserve (e.g. out.txt)"))

	def title(self):
		return "Keep file %s" % self.filename

	def run(self, env):
		path = os.path.join(env.tmpdir(),self.filename)

		result = self.create_result(env)
		if os.path.isfile(path):
			artefact = CheckerResultArtefact(result = result)
			artefact.file.save(self.filename, File(open(path)))
			result.set_passed(True)
		else:
			result.set_log("<p>Could not find file <tt>%s</tt>.</p>" % escape(self.filename))
			result.set_passed(False)

		return result

from checker.admin import	CheckerInline
class KeepFileCheckerInline(CheckerInline):
	model = KeepFileChecker

