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
			contenttype = mimetypes.guess_type(data.name)[0] # don't rely on the browser: data.content_type could be wrong or empty
			if not (SolutionFile.supported_types_re.match(contenttype) or ziptype_re.match(contenttype)):
				raise forms.ValidationError(_('The file of type %s is not supported.' %contenttype))
			if ziptype_re.match(contenttype):
				try:
					zip = zipfile.ZipFile(data)
					if zip.testzip():
						raise forms.ValidationError(_('The zip file seams to be corrupt.'))
					for fileinfo in zip.infolist():
						(type, encoding) = mimetypes.guess_type(fileinfo.filename)
						ignorred = SolutionFile.ignorred_file_names_re.match(fileinfo.filename)
						supported = type and SolutionFile.supported_types_re.match(type)
						if not ignorred and not supported:
							raise forms.ValidationError(_("The file '%(file)s' of guessed mime type '%(type)s' in this zip file is not supported." %{'file':fileinfo.filename, 'type':type}))
				except forms.ValidationError:
					raise
				except:
					raise forms.ValidationError(_('Uhoh - something unexpected happened.'))
			return data

class MyBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(MyBaseInlineFormSet, self).clean()
        if not reduce(lambda x,y: x + y.changed_data, self.forms, []):
			raise forms.ValidationError(_('You must at least choose one file.'))

SolutionFormSet = inlineformset_factory(Solution, SolutionFile, form=SolutionFileForm, formset=MyBaseInlineFormSet, can_delete=False, extra=3)
ModelSolutionFormSet = inlineformset_factory(Solution, SolutionFile, form=SolutionFileForm, formset=MyBaseInlineFormSet, can_delete=False, extra=1)