# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# This module collects all defaults settings for the praktomat
# It exports one function, load_defaults, which will set the settings in the
# parameter, but only if it is not already defined.

# The following variables have _no_ sane default, and need to be set!
no_defaults = [ "SITE_NAME", "PRAKTOMAT_ID", "BASE_HOST", "BASE_PATH", "UPLOAD_ROOT", "PRIVATE_KEY", "CERTIFICATE"]

import os
from os.path import dirname, join
import utilities.log_filter
import collections

def load_defaults(settings):
    missing = [ v for v in no_defaults if v not in settings]
    if missing:
        raise RuntimeError("Variables without defaults not set: %s" % ", ".join(missing))

    # import settings so that we can conveniently use the settings here
    for k, v in settings.items():
        try:
            from collections.abc import Callable  # noqa
        except ImportError:
            from collections import Callable  # noqa
        if not isinstance(v, Callable) and not k.startswith('__'):
            globals()[k] = v

    class D(object):

        def __setattr__(self, k, v):
            object.__setattr__(self, k, v)   # assign value v to instance attribute k
            if k not in globals():
                settings[k] = v
                globals()[k] = v
    d = D()

    # Absolute path to the praktomat source
    d.PRAKTOMAT_ROOT = dirname(dirname(dirname(__file__)))

    #############################################################################
    # Django Settings                                                           #
    #############################################################################

    # General setup

    # This will show debug information in the browser if an exception occurs.
    # Note that there are always going to be sections of your debug output that
    # are inappropriate for public consumption. File paths, configuration options,
    # and the like all give attackers extra information about your server.
    # Never deploy a site into production with DEBUG turned on.
    d.DEBUG = True

    # Local time zone for this installation. Choices can be found here:
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # although not all choices may be available on all operating systems.
    # If running in a Windows environment this must be set to the same as your
    # system time zone.
    d.TIME_ZONE = 'Europe/Berlin'

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    d.LANGUAGE_CODE = 'en-us'

    # A tuple that lists people who get code error notifications. When
    # DEBUG=False and a view raises an exception, Django will email these
    # people with the full exception information. Each member of the tuple
    # should be a tuple of (Full name, email address).
    d.ADMINS = []

    # A tuple in the same format as ADMINS that specifies who should get broken
    # link notifications when BrokenLinkEmailsMiddleware is enabled.
    d.MANAGERS = ADMINS

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    d.USE_I18N = True

    # Apps and plugins

    rhtmp=()
    # if Django_version  is ( 1.8, 1.9, 1.10, 1.11, 2.0)
    # insert 'admin_view_permission' as first element in d.INSTALLED_APPS
    from django import get_version as djv
    from distutils.version import StrictVersion
    if StrictVersion('1.8') <= StrictVersion(djv()) and StrictVersion(djv()) <= StrictVersion('2.0') :
        rhtmp = (
            'admin_view_permission',
        )
    d.INSTALLED_APPS = rhtmp + (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django.contrib.staticfiles',

        # ./manage.py runserver_plus allows for debugging on werkzeug traceback page. invoke error with assert false
        # not needed for production
        'django_extensions',

        # contains a widget to render a form field as a TinyMCE editor
        'tinymce',

        'configuration',
        'accounts',
        'tasks',
        'solutions',
        'attestation',
        'checker',
        'utilities',
        'settings',
        #'sessionprofile', #phpBB integration
        'taskstatistics',
    )

    d.MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',
        #'sessionprofile.middleware.SessionProfileMiddleware', #phpBB integration
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'accounts.middleware.AuthenticationMiddleware',
        'accounts.middleware.LogoutInactiveUserMiddleware',
        'accounts.middleware.DisclaimerAcceptanceMiddleware',
    ]

    d.DEFAULT_FILE_STORAGE = 'utilities.storage.UploadStorage'

    # URL and file paths
    # Template file path is set in template section

    d.STATICFILES_DIRS = (
        join(PRAKTOMAT_ROOT, "media"),
    )

    # collect static contents outside of Praktomat
    d.STATIC_ROOT = join(dirname(PRAKTOMAT_ROOT), "static")


    # This directory is used to compiling and running the users code.
    # As such it is temporary, and might be put on a tmpfs mount, to speed
    # up the processing
    d.SANDBOX_DIR = join(UPLOAD_ROOT, 'SolutionSandbox')

    d.ROOT_URLCONF = 'urls'

    d.LOGIN_REDIRECT_URL = 'task_list'

    # URL to use when referring to static files located in STATIC_ROOT.
    # Example: "/static/" or "http://static.example.com/"
    # If not None, this will be used as the base path for asset definitions
    # (the Media class) and the staticfiles app.
    # It must end in a slash if set to a non-empty value.
    d.STATIC_URL = BASE_PATH + 'static/'

    # The URL prefix for admin media - CSS, JavaScript and images used by the
    # Django administrative interface. Make sure to use a trailing slash, and to
    # have this be different from the MEDIA_URL setting (since the same URL cannot
    # be mapped onto two different sets of files). For integration with
    # staticfiles, this should be the same as STATIC_URL followed by 'admin/'.
    d.ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

    # Security

    d.SESSION_COOKIE_PATH = BASE_PATH

    d.CSRF_COOKIE_NAME = 'csrftoken_' + PRAKTOMAT_ID

    # Make this unique, and don't share it with anybody.
    if 'SECRET_KEY' not in globals():
        secret_keyfile = join(UPLOAD_ROOT, 'SECRET_KEY')
        if os.path.exists(secret_keyfile):
            with open(secret_keyfile) as f:
                d.SECRET_KEY = f.read()
            if not d.SECRET_KEY:
                raise RuntimeError("File %s empty!" % secret_keyfile)
        else:
            import uuid
            d.SECRET_KEY = uuid.uuid4().hex
            os.fdopen(os.open(secret_keyfile, os.O_WRONLY | os.O_CREAT, 0o600), 'w').write(d.SECRET_KEY)


    # Templates

    d.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                join(PRAKTOMAT_ROOT, "src", "templates"),
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'context_processors.settings.from_settings',
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.request',
                    'django.template.context_processors.static',
                    'django.contrib.messages.context_processors.messages',
                ],
                # A boolean that turns on/off template debug mode. If this is True, the fancy
                # error page will display a detailed report for any TemplateSyntaxError.
                # Note that Django only displays fancy error pages if DEBUG is True.
                'debug': True
            },
        },
    ]

    # Database

    d.DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME':   UPLOAD_ROOT+'/Database'
        }
    }

    # Email

    # Default email address to use for various automated correspondence from
    # the site manager(s).
    d.DEFAULT_FROM_EMAIL = ""
    d.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    d.EMAIL_HOST = "smtp.googlemail.com"
    d.EMAIL_PORT = 587
    d.EMAIL_HOST_USER = ""
    d.EMAIL_HOST_PASSWORD = ""
    d.EMAIL_USE_TLS = False

    # TinyMCE

    d.TINYMCE_JS_URL = STATIC_URL + 'frameworks/tiny_mce/tiny_mce_src.js'
    d.TINYMCE_DEFAULT_CONFIG = {
      'plugins': 'safari,pagebreak,table,advhr,advimage,advlink,emotions,iespell,inlinepopups,media,searchreplace,print,contextmenu,paste,fullscreen,noneditable,visualchars,nonbreaking,syntaxhl',

      'theme': "advanced",
      'theme_advanced_buttons1': "formatselect,|,bold,italic,underline,strikethrough,|,forecolor,|,bullist,numlist,|,sub,sup,|,outdent,indent,blockquote,syntaxhl,|,visualchars,nonbreaking,|,link,unlink,anchor,image,cleanup,help,code,|,print,|,fullscreen",
        'theme_advanced_buttons2': "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,tablecontrols,|,hr,removeformat,visualaid,|,charmap,emotions,iespell,media,advhr",
        'theme_advanced_buttons3': "",
        'theme_advanced_buttons4': "",
        'theme_advanced_toolbar_location': "top",
        'theme_advanced_toolbar_align': "left",
        'theme_advanced_statusbar_location': "bottom",
        'theme_advanced_resizing': True,
        'extended_valid_elements': "textarea[cols|rows|disabled|name|readonly|class]",

        'content_css': STATIC_URL + '/styles/style.css',
      'relative_urls': False,
    }
    d.TINYMCE_SPELLCHECKER = False
    d.TINYMCE_COMPRESSOR = False
    d.TINYMCE_INCLUDE_JQUERY = False

    #############################################################################
    # Praktomat-specific settings                                               #
    #############################################################################

    # Private key used to sign uploded solution files in submission confirmation email
    #d.PRIVATE_KEY = '/home/praktomat/certificates/privkey.pem'

    # Is this a mirror of another instance (different styling)
    d.MIRROR = False

    # The Compiler binarys used to compile a submitted solution
    d.C_BINARY = 'gcc'
    d.CXX_BINARY = 'c++'
    d.JAVA_BINARY = 'javac'
    d.JAVA_BINARY_SECURE = PRAKTOMAT_ROOT + '/src/checker/scripts/javac'
    d.JVM = 'java'
    d.JVM_SECURE = PRAKTOMAT_ROOT + '/src/checker/scripts/java'
    d.JVM_POLICY = PRAKTOMAT_ROOT + '/src/checker/scripts/java.policy'
    d.FORTRAN_BINARY = 'g77'
    d.ISABELLE_BINARY = 'isabelle' # Isabelle should be in PATH
    d.DEJAGNU_RUNTEST = '/usr/bin/runtest'
    d.CHECKSTYLEALLJAR = '/home/praktomat/contrib/checkstyle-8.14-all.jar'
    d.JUNIT38='junit'
    d.JAVA_LIBS = { 'jun' : '/usr/share/java/junit.jar', 'junit4' : '/usr/share/java/junit4.jar' }
    d.JAVA_CUSTOM_LIBS = PRAKTOMAT_ROOT + '/lib/java/*'
    d.JCFDUMP='jcf-dump'

    d.JAVAP='javap'
    d.GHC='ghc'
    d.SCALA='scala'
    d.SCALAC='scalac'

    # Enable to run all scripts (checker) as the unix user 'tester'. Therefore
    # put 'tester' as well as the Apache user '_www' (and your development user
    # account) into a new group called praktomat. Also edit your sudoers file
    # with "sudo visudo". Add the following lines to the end of the file to
    # allow the execution of commands with the user 'tester' without requiring
    # a password:
    # "_www            ALL=(tester)NOPASSWD:ALL"
    # "developer    ALL=(tester)NOPASSWD:ALL"
    d.USEPRAKTOMATTESTER = False

    # Alternatively: Run everything in a docker instance, to provide higher
    # insulation. Should not be used together with USEPRAKTOMATTESTER.

    # It is recomended to use DOCKER and not a tester account
    # for using Docker from https://github.com/nomeata/safe-docker
    # Use docker to test submission

    # To allow Praktomat the execution of scriptfile  safe-docker  without requiring a password:
    # "praktomat	ALL= NOPASSWD: /usr/local/bin/safe-docker"

    d.USESAFEDOCKER = False

    # The path where the safe-docker script is located
    # By default, it is assumed to be accessible through your PATH.
    d.SAFE_DOCKER_PATH = "safe-docker"

    # The name of the Docker image to use for executing checkers
    d.DOCKER_IMAGE_NAME = "safe-docker"

    # If the file system of the Docker container should be writable or read-only
    d.DOCKER_CONTAINER_WRITABLE = False

    # If the UID and GID of the user in a Docker container should be set to the one running Praktomat
    # When this is set to false, checkers may run as root (depending on the image).
    d.DOCKER_UID_MOD = True

    # The path which to additionally mount into the checker container
    # If this is set to none, no additional directory will get mounted.
    d.DOCKER_CONTAINER_EXTERNAL_DIR = None


    # be sure that you change file permission
    # sudo chown praktomat:tester praktomat/src/checker/scripts/java
    # sudo chown praktomat:tester praktomat/src/checker/scripts/javac
    # sudo chmod u+x,g+x,o-x praktomat/src/checker/scripts/java
    # sudo chmod u+x,g+x,o-x praktomat/src/checker/scripts/javac

    # Make sure uploaded solution are not work-readable
    d.FILE_UPLOAD_PERMISSIONS = 0o640

    # This enables Shibboleth support.
    # In order to actually get it working, you need to protect the location
    # .../accounts/shib_login in the apache configuration, e.g. with this
    # stanca:
    #    <Location /shibtest/accounts/shib_login>
    #        Order deny,allow
    #        AuthType shibboleth
    #        ShibRequireSession On
    #        Require valid-user
    #    </Location>
    #
    # You probably want to disable REGISTRATION_POSSIBLE if you enable
    # Shibboleth support
    d.SHIB_ENABLED = False

    d.SHIB_ATTRIBUTE_MAP = {
        "mail": (True, "email"),
        "givenName": (True, "first_name"),
        "sn": (True, "last_name"),
        "matriculationNumber": (False, "matriculationNumber"),
        "fieldOfStudyText": (False, "programme"),
    }

    d.SHIB_USERNAME = "email"
    d.SHIB_PROVIDER = "kit.edu"

    # URL to the MOTD page which will be shown on login page and task list
    d.SYSADMIN_MOTD_URL = None

    # Set this to False to disable registration via the website, e.g. when
    # Single Sign On is used
    d.REGISTRATION_POSSIBLE = True

    # Set this to False to disable "Got Problems?"-link in task list
    d.SHOW_CONTACT_LINK = True

    # Set this to False to disable account changes via the website
    d.ACCOUNT_CHANGE_POSSIBLE = True

    # Set this to True to automatically set user.mat_number = user.id
    d.DUMMY_MAT_NUMBERS = False

    # needed since Django 1.11 in order to show the 'Deactivated' page
    d.AUTH_BACKEND = 'django.contrib.auth.backends.AllowAllUsersModelBackend'

    #TODO: Code refactoring: make it more flexible, to change between LDAP or Shibboleth support!

    # LDAP support
    # You probably want to disable REGISTRATION_POSSIBLE if you enable LDAP
    # LDAP config put it in local or devel settings with individual correct values!

    d.LDAP_ENABLED = False
    d.AUTHENTICATION_BACKENDS = (
	    'accounts.ldap_auth.LDAPBackend',
	    d.AUTH_BACKEND,
    )
    d.LDAP_URI="ldap://ldap.DOMAINNAME.TOPLEVEL"
    d.LDAP_BASE="dc=DOMAINNAME,dc=TOPLEVEL"


    # Length of timeout applied whenever an external check that runs a students
    # submission is executed,
    # for example: JUnitChecker, DejaGnuChecker
    d.TEST_TIMEOUT=60  # but make sure to use ulimit -t 60 inside shell scripts!

    # Amount of memory available to the checker, in megabytes
    # (this is currently only supported with USESAFEDOCKER=True)
    d.TEST_MAXMEM=100

    # Maximal size (in kbyte) of files created whenever an external check that
    # runs a students submission is executed,
    # for example: JUnitChecker, DejaGnuChecker
    d.TEST_MAXFILESIZE=64

    # Maximal size (in kbyte) of checker logs accepted. This setting is
    # respected currently only by:
    # JUnitChecker, ScriptChecker,
    d.TEST_MAXLOGSIZE=64

    # Maximum number of open file descriptors for a checker.
    d.TEST_MAXFILENUMBER=128

    d.NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 1

    d.MIMETYPE_ADDITIONAL_EXTENSIONS = \
        [("text/plain", ".properties"),
         ("text/x-gradle", ".gradle"),
         ("text/x-gradle", ".gradle.kts"),
         ("text/x-isabelle", ".thy"),
         ("text/x-lean", ".lean"),
         ("text/x-r-script", ".R"),
         ("text/x-r-script", ".r"),# Fixes KITPraktomatTeam/Praktomat#336 as workaround for issue in Python 3.9.12 and above: Add filename extension with small letter r to dict of additional mimetypes , more information see issue Python stdlib  92455
         ]

    # Subclassed TestSuitRunner to prepopulate unit test database.
    d.TEST_RUNNER = 'utilities.TestSuite.TestSuiteRunner'

    # This is actually a django setting, but depends on a praktomat setting:
    if SHIB_ENABLED:
        d.LOGIN_URL = 'shib_hello'
    else:
        d.LOGIN_URL = 'login'

    if DEBUG:
        # Setup for the debug toolbar
        settings['INSTALLED_APPS'] = ('debug_toolbar',) + settings['INSTALLED_APPS']
        settings['MIDDLEWARE'] = [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        ] + settings['MIDDLEWARE']

    d.DEBUG_TOOLBAR_PATCH_SETTINGS = False
    d.DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'settings.defaults.show_toolbar',
    }

    d.LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'skip_unreadable_posts': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': utilities.log_filter.skip_unreadable_post,
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['skip_unreadable_posts'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
    }

# Always show toolbar (if DEBUG is true)
def show_toolbar(request):
    if request.is_ajax():
        return False

    # return True here to enable the debug toolbar
    return True
