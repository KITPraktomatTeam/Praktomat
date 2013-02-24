#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.base'
os.environ['PRAKTOMAT_SETTINGS'] = 'local'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# vim:ft=python
