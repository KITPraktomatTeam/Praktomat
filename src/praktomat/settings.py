# -*- coding: utf-8 -*-
# General settings for praktomat project.

import os

# A boolean that turns on/off template debug mode. If this is True, the fancy 
# error page will display a detailed report for any TemplateSyntaxError. 
# Note that Django only displays fancy error pages if DEBUG is True.
TEMPLATE_DEBUG = True

# Subclassed TestSuitRunner to prepopulate unit test database.
TEST_RUNNER = 'praktomat.utilities.TestSuite.TestSuiteRunner'

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

TEMPLATE_CONTEXT_PROCESSORS = (
    "praktomat.context_processors.current_site.current_site",
    "django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.contrib.messages.context_processors.messages"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'praktomat.accounts.middleware.AuthenticationMiddleware',
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
	
    # intelligent schema and data migrations
    'south', 
    
    # contains a widget to render a form field as a TinyMCE editor
    'tinymce',
	
	'praktomat.pagechunks',
	'praktomat.accounts',
  'praktomat.tasks',
	'praktomat.solutions',
	'praktomat.attestation',
	'praktomat.checker',
	'praktomat.utilities',
)


LOGIN_REDIRECT_URL = '/tasks/'

ACCOUNT_ACTIVATION_DAYS = 5


try:
    from settings_local import * 
except ImportError: 
    pass 

# TinyMCE
TINYMCE_JS_URL = MEDIA_URL+'frameworks/tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'safari,pagebreak,table,advhr,advimage,advlink,emotions,iespell,inlinepopups,media,searchreplace,print,contextmenu,paste,fullscreen,noneditable,visualchars,nonbreaking,syntaxhl',
    
    'theme': "advanced",
    'theme_advanced_buttons1' : "formatselect,|,bold,italic,underline,strikethrough,|,forecolor,|,bullist,numlist,|,sub,sup,|,outdent,indent,blockquote,syntaxhl,|,visualchars,nonbreaking,|,link,unlink,anchor,image,cleanup,help,code,|,print,|,fullscreen",
	'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,tablecontrols,|,hr,removeformat,visualaid,|,charmap,emotions,iespell,media,advhr",				   
	'theme_advanced_buttons3' : "",
	'theme_advanced_buttons4' : "",
	'theme_advanced_toolbar_location' : "top",
	'theme_advanced_toolbar_align' : "left",
	'theme_advanced_statusbar_location' : "bottom",
	'theme_advanced_resizing' : True,
	'extended_valid_elements' : "textarea[cols|rows|disabled|name|readonly|class]" ,
	
	'content_css' : MEDIA_URL+'/styles/style.css',
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False

# MEDIA_ROOT is a missguiding name django uses as default for it's upload location
MEDIA_ROOT = UPLOAD_ROOT
