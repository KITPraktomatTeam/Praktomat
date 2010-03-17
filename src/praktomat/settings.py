# -*- coding: utf-8 -*-
# General settings for praktomat project.

import os

# A boolean that turns on/off template debug mode. If this is True, the fancy 
# error page will display a detailed report for any TemplateSyntaxError. 
# Note that Django only displays fancy error pages if DEBUG is True.
TEMPLATE_DEBUG = True

# The ID, as an integer, of the current site in the django_site database table. 
# This is used so that application data can hook into specific site(s) and 
# a single database can manage content for multiple sites.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'db(@293vg@52-2mgn2zjypq=pc@28t@==$@@vt^yf78l$429yn'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'praktomat.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__),"templates")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',	
    'django.contrib.admin',
    'django.contrib.admindocs',
	'django.contrib.markup',

	# ./manage.py runserver_plus allows for debugging on werkzeug traceback page. invoke error with assert false
	# not needed for production
	'django_extensions',
	
	# the concurrent test server allows to make an ajax request to the server while the server handles an other request
	# example: getting the upload status while the server runs all checker
	# http://github.com/jaylett/django_concurrent_test_server
	# no need to install the app, its allready in the praktomat folder
	# ./manage.py runconcurrentserver
	#'django_concurrent_test_server',
	
	'praktomat.accounts',
    'praktomat.tasks',
	'praktomat.solutions',
	'praktomat.attestation',
	'praktomat.checker',
)


LOGIN_REDIRECT_URL = '/tasks/'

ACCOUNT_ACTIVATION_DAYS = 5

try: 
    from settings_local import * 
except ImportError: 
    pass 

from django.core.files.storage import FileSystemStorage
STORAGE = FileSystemStorage(location=UPLOAD_ROOT, base_url=UPLOAD_URL)