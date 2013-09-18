#!/usr/bin/env python
import os
from os.path import join, dirname
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'

import site
site.addsitedir(join(dirname(dirname(dirname(__file__))), "env", "lib", "python2.7","site-packages"))

import sys
sys.path.append(join(dirname(dirname(__file__)), "src"))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# vim:ft=python
