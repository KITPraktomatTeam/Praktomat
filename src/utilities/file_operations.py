# -*- coding: utf-8 -*-

import os
import grp
import tempfile
from django.conf import settings
from utilities import encoding

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


def create_file(path, content, replace=[], override=True):
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
	for (old, new) in replace:
		content.replace(old, new)
	with open(path, 'w') as fd:
		fd.write(encoding.get_utf8(content))
	if (gid):
		# chown :praktomat <path>
		os.chown(path, -1, gid)		
		# rwxrwx--- 	access for praktomattester:praktomat
		os.chmod(path, 0770)			


def copy_file(from_file_path, to_file_path, replace=[], override=True):
	""" """
	with open(from_file_path) as fd:
		content = encoding.get_unicode(fd.read())
	create_file(to_file_path, content, replace=replace, override=override)


def copy_file_to_directory_verbatim(from_path, to_path, override=True):
	to_path = os.path.join(to_path, os.path.basename(from_path))
	dirname = os.path.dirname(to_path)
	if not os.path.exists(dirname):
		makedirs(dirname)
	else:
		if os.path.exists(to_path):
			if override: # delete file
				os.remove(to_path)
			else: # throw exception
				raise Exception('File already exists')
	with open(to_path, 'w') as fdout, open(from_path, 'r') as fdin:
		fdout.write(fdin.read())
	if (gid):
		# chown :praktomat <path>
		os.chown(to_path, -1, gid)		
		# rwxrwx--- 	access for praktomattester:praktomat
		os.chmod(to_path, 0770)



def copy_file_to_directory(from_file_path, to_path, replace=[], override=True):
	copy_file(from_file_path, os.path.join(to_path, os.path.basename(from_file_path)), replace=replace, override=override)


def create_tempfolder(path):
	makedirs(path)
	tempfile.tempdir = path
	new_tmpdir = tempfile.mkdtemp()
	if (gid):
		os.chown(new_tmpdir, -1, gid)
	os.chmod(new_tmpdir, 0770)	
	return new_tmpdir

	
