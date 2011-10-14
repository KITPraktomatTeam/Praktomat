# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.forms.models import ModelForm, inlineformset_factory, BaseInlineFormSet
from django import forms
import zipfile
import mimetypes
import re

from solutions.models import Solution, SolutionFile
						
ziptype_re = re.compile(r'^application/(zip|x-zip|x-zip-compressed|x-compressed)$')						

class SolutionFileForm(ModelForm):
	class Meta:
		model = SolutionFile
		exclude = ('mime_type',)
		
	def clean_file(self):
		data = self.cleaned_data['file']
		task = self.cleaned_data['solution'].task
		max_file_size_kb = task.max_file_size
		max_file_size = 1024 * max_file_size_kb
		supported_types_re = re.compile(task.supported_file_types)
		if data:
			contenttype = mimetypes.guess_type(data.name)[0] # don't rely on the browser: data.content_type could be wrong or empty
			if (contenttype is None) or (not (supported_types_re.match(contenttype) or ziptype_re.match(contenttype))):
				raise forms.ValidationError(_('The file of type %s is not supported.' %contenttype))
			if ziptype_re.match(contenttype):
				try:
					zip = zipfile.ZipFile(data)
					if zip.testzip():
						raise forms.ValidationError(_('The zip file seams to be corrupt.'))
					if sum(fileinfo.file_size for fileinfo in zip.infolist()) > 1000000:
						raise forms.ValidationError(_('The zip file is to big.'))	
					for fileinfo in zip.infolist():
						(type, encoding) = mimetypes.guess_type(fileinfo.filename)
						ignorred = SolutionFile.ignorred_file_names_re.search(fileinfo.filename)
						supported = type and supported_types_re.match(type)
						if not ignorred and not supported:
							raise forms.ValidationError(_("The file '%(file)s' of guessed mime type '%(type)s' in this zip file is not supported." %{'file':fileinfo.filename, 'type':type}))
						# check whole zip instead of contained files
						#if fileinfo.file_size > max_file_size:
						#	raise forms.ValidationError(_("The file '%(file)s' is bigger than %(size)iKB which is not suported." %{'file':fileinfo.filename, 'size':max_file_size_kb}))
				except forms.ValidationError:
					raise
				except:
					raise forms.ValidationError(_('Uhoh - something unexpected happened.'))
			if data.size > max_file_size:
				raise forms.ValidationError(_("The file '%(file)s' is bigger than %(size)iKB which is not suported." %{'file':data.name, 'size':max_file_size_kb}))
			return data

class MyBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(MyBaseInlineFormSet, self).clean()
        if not reduce(lambda x,y: x + y.changed_data, self.forms, []):
			raise forms.ValidationError(_('You must at least choose one file.'))

SolutionFormSet = inlineformset_factory(Solution, SolutionFile, form=SolutionFileForm, formset=MyBaseInlineFormSet, can_delete=False, extra=3)
ModelSolutionFormSet = inlineformset_factory(Solution, SolutionFile, form=SolutionFileForm, formset=MyBaseInlineFormSet, can_delete=False, extra=1)
