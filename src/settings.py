# -*- coding: utf-8 -*-
# General settings for praktomat project.

import os

# A boolean that turns on/off template debug mode. If this is True, the fancy 
# error page will display a detailed report for any TemplateSyntaxError. 
# Note that Django only displays fancy error pages if DEBUG is True.
TEMPLATE_DEBUG = True

# Subclassed TestSuitRunner to prepopulate unit test database.
TEST_RUNNER = 'utilities.TestSuite.TestSuiteRunner'

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
	'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'context_processors.settings.from_settings',
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
	'djangohelper.context_processors.ctx_config',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'accounts.middleware.AuthenticationMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
	'pagination.middleware.PaginationMiddleware',
	'onlineuser.middleware.OnlineUserMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.dirname(__file__)+"/templates",
	os.path.dirname(__file__)+"/lbforum/templates"
				 
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
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
				  
  	# Forum
	'pagination',
	'lbforum',
	'simpleavatar',
	'djangohelper',
	'onlineuser',
  	'attachments',

	'configuration',
	'accounts',
	'tasks',
	'solutions',
	'attestation',
	'checker',
	'utilities',
)


LOGIN_REDIRECT_URL = '/tasks/'

ACCOUNT_ACTIVATION_DAYS = 5

DEFAULT_FILE_STORAGE = 'utilities.storage.UploadStorage'

try:
    from settings_local import * 
except ImportError: 
    pass 

# Required to be set when baseurl ist not a top level domain
LOGIN_URL = BASE_URL + 'accounts/login/'
LOGIN_REDIRECT_URL = BASE_URL + 'tasks/'

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

# Forum
# URL prefix for lbforum media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
LBFORUM_MEDIA_PREFIX = '/media/lbforum/'


#The URL where requests are redirected for login
LOGIN_URL = "/accounts/login/"
#LOGIN_URL counterpart
LOGOUT_URL = "/accounts/logout/"
#register url
REGISTER_URL = "/accounts/register/"

CTX_CONFIG = {
	'LBFORUM_TITLE': 'Forum',
	'LBFORUM_SUB_TITLE': 'Praktomat Support Forum',
	'FORUM_PAGE_SIZE': 50,
	'TOPIC_PAGE_SIZE': 20,
	
	'LBFORUM_MEDIA_PREFIX': LBFORUM_MEDIA_PREFIX,
	'LOGIN_URL': LOGIN_URL,
	'LOGOUT_URL': LOGOUT_URL,
	'REGISTER_URL': REGISTER_URL,
}

BBCODE_AUTO_URLS = True
#add allow tags
HTML_SAFE_TAGS = ['embed']
HTML_SAFE_ATTRS = ['allowscriptaccess', 'allowfullscreen', 'wmode']
#add forbid tags
HTML_UNSAFE_TAGS = []
HTML_UNSAFE_ATTRS = []

"""
	#default html safe settings
	acceptable_elements = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
    'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
    'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
    'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
    'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
    'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
    'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
    'thead', 'tr', 'tt', 'u', 'ul', 'var']
	acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
    'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
    'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
    'colspan', 'color', 'compact', 'coords', 'datetime', 'dir',
    'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
    'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
    'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt',
    'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
    'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
    'usemap', 'valign', 'value', 'vspace', 'width', 'style']
	"""
