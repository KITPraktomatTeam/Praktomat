# -*- coding: utf-8 -*-

import os
import grp
import tempfile
from django.conf import settings
from utilities import encoding
import shutil
import zipfile

gid = None
if (settings.USEPRAKTOMATTESTER):
	gid = grp.getgrnam('praktomat').gr_gid


def makedirs(path):
	if os.path.exists(path):
		return
	else:
		(head,tail) = os.path.split(path)
		makedirs(head)
		os.mkdir(path)
		if (gid):
			os.chown(path, -1, gid)
		os.chmod(path, 0770)


def create_file(path, content, override=True, binary=False):
	""" """	
	dirname = os.path.dirname(path)
	if not os.path.exists(dirname):
		makedirs(dirname)
	else:
		if os.path.exists(path):
			if override: # delete file
				os.remove(path)
			else: # throw exception
				raise Exception('File already exists')
	with open(path, 'w') as fd:
		if binary:
			fd.write(content)
		else:
			fd.write(encoding.get_utf8(encoding.get_unicode(content)))
	if (gid):
		# chown :praktomat <path>
		os.chown(path, -1, gid)		
		# rwxrwx--- 	access for praktomattester:praktomat
		os.chmod(path, 0770)			


def copy_file(from_path, to_path, to_is_directory=False, override=True, binary=False):
	""" """
	if to_is_directory:
		to_path = os.path.join(to_path, os.path.basename(from_path))
	with open(from_path) as fd:
		create_file(to_path, fd.read(), override=override, binary=binary)


def create_tempfolder(path):
	makedirs(path)
	tempfile.tempdir = path
	new_tmpdir = tempfile.mkdtemp()
	if (gid):
		os.chown(new_tmpdir, -1, gid)
	os.chmod(new_tmpdir, 0770)	
	return new_tmpdir

class InvalidZipFile(Exception):
	pass

def unpack_zipfile_to(zipfilename, to_path, override_cb=None, file_cb=None):
	"""
	Extracts a zipfile to the given location, trying to safeguard against wrong paths

	The override_cb is called for every file that overwrites an existing file,
	with the name of the file in the archive as the parameter.

	The file_cb is called for every file, after extracting it.
	"""	
	if not zipfile.is_zipfile(zipfilename):
		raise InvalidZipFile("File %s is not a zipfile." % zipfilename)
	zip = zipfile.ZipFile(zipfilename, 'r')
	
	if zip.testzip():
		raise InvalidZipFile("File %s is invalid." % zipfilename)

	# zip.extractall would not protect against ..-paths,
	# it would do so from python 2.7.4 on.
	for finfo in zip.infolist():
		dest = os.path.join(to_path, finfo.filename)

		# This check is from http://stackoverflow.com/a/10077309/946226
		if not os.path.realpath(os.path.abspath(dest)).startswith(to_path):
			raise InvalidZipFile("File %s contains illegal path %s." % (zipfilename, finfo.filename))
		if override_cb is not None and os.path.exists(dest):
			override_cb(finfo.filename)
		zip.extract(finfo, to_path)
		if file_cb is not None and os.path.isfile(os.path.join(to_path,finfo.filename)):
			file_cb(finfo.filename)
