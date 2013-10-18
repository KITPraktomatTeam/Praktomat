# -*- coding: utf-8 -*-

import os
import grp
import tempfile
from django.conf import settings
from utilities import encoding
import shutil

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

	
