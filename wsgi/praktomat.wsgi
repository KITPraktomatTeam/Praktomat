#!/usr/bin/env python3
import os
from os.path import join, dirname, basename
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'

import pathlib
env_lib_path = pathlib.Path(join(dirname(dirname(dirname(__file__))), "env", "lib"))
subdirs = [str(p) for p in env_lib_path.iterdir() if p.is_dir()]
python_path = [p for p in subdirs if basename(p).startswith("python3.")][0]
import site
site.addsitedir(join(python_path, "site-packages"))

import sys
sys.path.append(join(dirname(dirname(__file__)), "src"))

import warnings
from django.core.cache import CacheKeyWarning
warnings.simplefilter("ignore", CacheKeyWarning)

import resource
def set_to_hard(res):
	(s,h) = resource.getrlimit(res)
	resource.setrlimit(res,(h,h))
set_to_hard(resource.RLIMIT_AS)
set_to_hard(resource.RLIMIT_NPROC)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# vim:ft=python
