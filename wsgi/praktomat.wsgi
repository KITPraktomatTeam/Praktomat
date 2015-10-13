#!/usr/bin/env python
import os
from os.path import join, dirname
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'

import site
site.addsitedir(join(dirname(dirname(dirname(__file__))), "env", "lib", "python2.7","site-packages"))

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
