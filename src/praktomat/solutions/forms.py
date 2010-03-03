# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.forms.models import ModelForm, inlineformset_factory, BaseInlineFormSet
from django import forms
import zipfile
import mimetypes
import re

from praktomat.solutions.models import Solution, SolutionFile
						
ziptype_re = re.compile(r'^application/(zip|x-zip|x-zip-compressed|x-compressed)$')						

class SolutionFileForm(ModelForm):
	class Meta:
		model = SolutionFile
		
	def clean_file(self):
		data = self.cleaned_data['file']
		if data:
			if not (SolutionFile.supported_types_re.match(data.content_type) or ziptype_re.match(data.content_type)):
				raise forms.ValidationError(_('The file of Type %s is not supported.' %data.content_type))
			if ziptype_re.match(data.content_type):
				try:
					zip = zipfile.ZipFile(data)
					if zip.testzip():
						raise forms.ValidationError(_('The zipfile seams to be corrupt.'))
					for fileinfo in zip.infolist():
						(type, encoding) = mimetypes.guess_type(fileinfo.filename)
						ignorred = SolutionFile.ignorred_file_names_re.match(fileinfo.filename)
						supported = type and SolutionFile.supported_types_re.match(type)
						if not ignorred and not supported:
							raise forms.ValidationError(_('The file %(file)s of Type %(type)s in this zipfile is not supported.' %{'file':fileinfo.filename, 'type':type}))
				except:
					raise forms.ValidationError(_('The zipfile seams to be corrupt.'))
			return data

class MyBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(MyBaseInlineFormSet, self).clean()
        if not reduce(lambda x,y: x + y.changed_data, self.forms, []):
			raise forms.ValidationError(_('You must at least choose one file.'))

SolutionFormSet = inlineformset_factory(Solution, SolutionFile, form=SolutionFileForm, formset=MyBaseInlineFormSet, can_delete=False, extra=3)