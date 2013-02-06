# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.forms.models import ModelForm, inlineformset_factory, BaseInlineFormSet
from django import forms
from django.conf import settings
import zipfile
import tarfile
import mimetypes
import re

from solutions.models import Solution, SolutionFile
						
ziptype_re = re.compile(r'^application/(zip|x-zip|x-zip-compressed|x-compressed)$')	
tartype_re = re.compile(r'^application/(tar|x-tar|x-tar-compressed)$')	

for (mimetype,extension) in settings.MIMETYPE_ADDITIONAL_EXTENSIONS:
	mimetypes.add_type(mimetype,extension,strict=True)

class SafeUncompressor(object):
	"""Small proxy class that enables external file object
	support for uncompressed, bzip2 and gzip files. Works transparently, and
	supports a maximum size to avoid zipbombs.
	"""
	blocksize = 16 * 1024

	class FileTooLarge(Exception):
		pass

	def __init__(self, fileobj, maxsize=10*1024*1024):
		self.fileobj = fileobj
		self.name = getattr(self.fileobj, "name", None)
		self.maxsize = maxsize
		self.init()

	def init(self):
		import bz2
		import gzip
		self.pos = 0
		self.fileobj.seek(0)
		self.buf = ""
		self.format = "plain"

		magic = self.fileobj.read(2)
		if magic == '\037\213':
			self.format = "gzip"
			self.gzipobj = gzip.GzipFile(fileobj = self.fileobj, mode = 'r')
		elif magic == 'BZ':
			raise IOError, "bzip2 support in SafeUncompressor disabled, as self.bz2obj.decompress is not safe"
			self.format = "bz2"
			self.bz2obj = bz2.BZ2Decompressor()
		self.fileobj.seek(0)
			

	def read(self, size):
		b = [self.buf]
		x = len(self.buf)
		while x < size:
			if self.format == 'gzip':
				data = self.gzipobj.read(self.blocksize)
				if not data:
					break
			elif self.format == 'bz2':
				raw = self.fileobj.read(self.blocksize)
				if not raw:
					break
				# this can already bomb here, to some extend.
				# so disable bzip support until resolved.
				# Also monitor http://stackoverflow.com/questions/13622706/how-to-protect-myself-from-a-gzip-or-bzip2-bomb for ideas
				data = self.bz2obj.decompress(raw)
			else:
				data = self.fileobj.read(self.blocksize)
				if not data:
					break
			b.append(data)
			x += len(data)

			if self.pos + x > self.maxsize:
				self.buf = ""
				self.pos = 0
				raise SafeUncompressor.FileTooLarge, "Compressed file too large"
		self.buf = "".join(b)

		buf = self.buf[:size]
		self.buf = self.buf[size:]
		self.pos += len(buf)
		return buf

	def seek(self, pos, whence=0):
		if whence != 0:
			raise IOError, "SafeUncompressor only supports whence=0"
		if pos < self.pos:
			self.init()
		self.read(pos - self.pos)

	def tell(self):
		return self.pos

	def write(self, data):
		self.pos += len(data)
		raw = self.bz2obj.compress(data)
		self.fileobj.write(raw)

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
			if (contenttype is None) or (not (supported_types_re.match(contenttype) or ziptype_re.match(contenttype) or tartype_re.match(contenttype))):
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
			elif tartype_re.match(contenttype):
				try:
					uncompressed = SafeUncompressor(data, max_file_size);
					tar = tarfile.open(mode = 'r:', fileobj = uncompressed)
					#if tar.testtar():
					#	raise forms.ValidationError(_('The tar file seams to be corrupt.'))
					if sum(fileinfo.size for fileinfo in tar.getmembers()) > 1000000:
						raise forms.ValidationError(_('The tar file is to big.'))
					for fileinfo in tar.getmembers():
						if not fileinfo.isfile():
							continue
						(type, encoding) = mimetypes.guess_type(fileinfo.name)
						ignorred = SolutionFile.ignorred_file_names_re.search(fileinfo.name)
						supported = type and supported_types_re.match(type)
						if not ignorred and not supported:
							raise forms.ValidationError(_("The file '%(file)s' of guessed mime type '%(type)s' in this tar file is not supported." %{'file':fileinfo.name, 'type':type}))
						# check whole tar instead of contained files
						#if fileinfo.file_size > max_file_size:
						#	raise forms.ValidationError(_("The file '%(file)s' is bigger than %(size)iKB which is not suported." %{'file':fileinfo.name, 'size':max_file_size_kb}))
					data.seek(0)
				except forms.ValidationError:
					raise
				except SafeUncompressor.FileTooLarge:
					raise forms.ValidationError(_('The tar file is to big.'))
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
