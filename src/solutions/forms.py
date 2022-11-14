# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.forms.models import ModelForm, inlineformset_factory, BaseInlineFormSet
from django import forms
from django.conf import settings
import zipfile
import mimetypes
import re

from solutions.models import Solution, SolutionFile
from utilities import encoding
from functools import reduce

ziptype_re = re.compile(r'^application/(zip|x-zip|x-zip-compressed|x-compressed)$')
tartype_re = re.compile(r'^application/(tar|x-tar|x-tar-compressed)$')

for (mimetype, extension) in settings.MIMETYPE_ADDITIONAL_EXTENSIONS:
    mimetypes.add_type(mimetype, extension, strict=True)

def contains_NUL_char(bytestring):
    return encoding.get_unicode(bytestring).find("\x00") >= 0

class SolutionFileForm(ModelForm):
    class Meta:
        model = SolutionFile
        exclude = ('mime_type',)

    def clean_file(self):
        data = self.cleaned_data['file']
        task = self.cleaned_data['solution'].task
        max_file_size_kib = task.max_file_size
        max_file_size = 1024 * max_file_size_kib
        supported_types_re = re.compile(task.supported_file_types)
        if data:
            contenttype = mimetypes.guess_type(data.name)[0] # don't rely on the browser: data.content_type could be wrong or empty
            if (contenttype is None) or (not (supported_types_re.match(contenttype) or ziptype_re.match(contenttype) or tartype_re.match(contenttype))):
                raise forms.ValidationError(_('The file of type %s is not supported.' %contenttype))
            if contenttype.startswith("text"):
                content = data.read()
                # undo the consuming the read method has done
                data.seek(0)
                if contains_NUL_char(content):
                    raise forms.ValidationError(_("The plain text file '%(file)s' contains a NUL character, which is not supported." %{'file':data.name}))
            if ziptype_re.match(contenttype):
                try:
                    zip = zipfile.ZipFile(data)
                    if zip.testzip():
                        raise forms.ValidationError(_('The zip file seems to be corrupt.'))
                    if sum(fileinfo.file_size for fileinfo in zip.infolist()) > max_file_size:
                        # Protect against zip bombs
                        raise forms.ValidationError(_('The zip file is too big.'))
                    for fileinfo in zip.infolist():
                        filename = fileinfo.filename
                        (type, encoding) = mimetypes.guess_type(filename)
                        ignorred = SolutionFile.ignorred_file_names_re.search(filename)
                        supported = type and supported_types_re.match(type)
                        is_text_file = not ignorred and type and type.startswith("text")
                        if not ignorred and not supported:
                            raise forms.ValidationError(_("The file '%(file)s' of guessed mime type '%(type)s' in this zip file is not supported." %{'file':filename, 'type':type}))
                        if is_text_file and contains_NUL_char(zip.read(filename)):
                            raise forms.ValidationError(_("The plain text file '%(file)s' in this zip file contains a NUL character, which is not supported." %{'file':filename}))
                        # check whole zip instead of contained files
                        #if fileinfo.file_size > max_file_size:
                        #    raise forms.ValidationError(_("The file '%(file)s' is bigger than %(size)KiB which is not suported." %{'file':fileinfo.filename, 'size':max_file_size_kib}))
                except forms.ValidationError:
                    raise
                except:
                    raise forms.ValidationError(_('Uhoh - something unexpected happened.'))
            elif tartype_re.match(contenttype):
                raise forms.ValidationError(_('Tar files are not supported, please upload the files individually or use a zip file.'))
            if data.size > max_file_size:
                raise forms.ValidationError(_("The file '%(file)s' is bigger than %(size)d KiB which is not supported." %{'file':data.name, 'size':max_file_size_kib}))
            return data

class MyBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(MyBaseInlineFormSet, self).clean()
        if not reduce(lambda x, y: x + y.changed_data, self.forms, []):
            raise forms.ValidationError(_('You must choose at least one file.'))

SolutionFormSet = inlineformset_factory(Solution, SolutionFile, form=SolutionFileForm, formset=MyBaseInlineFormSet, can_delete=False, extra=1)
ModelSolutionFormSet = inlineformset_factory(Solution, SolutionFile, form=SolutionFileForm, formset=MyBaseInlineFormSet, can_delete=False, extra=1)
