# Settings for deployment

# These settings are HBRS-specific and derive some parts of the settings
# from the directory name.
#
# If you are not deploying on praktomat.inf.h-brs.de you need to rewrite this file.

from os.path import join, dirname, basename
import re

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))

#PRAKTOMAT_ID = basename(dirname(PRAKTOMAT_PATH))
#
#match = re.match(r'''
#	(?:praktomat_)?
#	(?P<algo1>algo1_)?
#	(?P<cram>cram_)?
#	(?P<year>\d+)_
#	(?P<semester>WS|SS)
#	(?P<abschluss>_Abschluss)?
#	(?P<mirror>_Mirror)?
#	''', PRAKTOMAT_ID, flags=re.VERBOSE)
#if match:
#	if match.group('algo1') is not None:
#		SITE_NAME = 'Algorithmen I '
#	elif match.group('cram') is not None:
#		SITE_NAME = 'CRAM '
#	else:
#		SITE_NAME = 'Programmieren '
#
#	if match.group('abschluss'):
#		SITE_NAME += "Abschlussaufgaben "
#
#	year = int(match.group('year'))
#	if match.group('semester') == "WS":
#		SITE_NAME += "Wintersemester %d/%d" % (year, year+1)
#	else:
#		SITE_NAME += "Sommersemester %d" % year
#
#	if match.group('mirror') is not None:
#		SITE_NAME += " (Mirror)"
#		MIRROR = True
#	else:
#		MIRROR = False
#else:
#	raise NotImplementedError("Autoconfig for PRAKTOMAT_ID %s not possible", PRAKTOMAT_ID)

# Hard overwriting Praktomat_id 
# Identifie this Praktomat among multiple installation on one webserver
PRAKTOMAT_ID = '2016s' 

# The name that will be displayed on top of the page and in emails.
SITE_NAME = 'Praktomat Sommersemester 2016 (AlgoDat)'



# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# developmentserver.
#BASE_HOST = 'https://praktomat.cs.kit.edu'
BASE_HOST = 'https://praktomattest.inf.h-brs.de/'
BASE_PATH = '/' + PRAKTOMAT_ID + '/'

#ALLOWED_HOSTS = [ 'praktomat.cs.kit.edu', ]
ALLOWED_HOSTS = [ 'praktomattest.inf.h-brs.de', ]

# URL to use when referring to static files.
STATIC_URL = BASE_PATH + 'static/'

STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")

#if "cram" in PRAKTOMAT_ID:
#  TEST_TIMEOUT=600

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
# UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "PraktomatSupport/")
# UPLOAD_ROOT = "/home/praktomat/inst/" + PRAKTOMAT_ID + "/work/"
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "work/")


#SANDBOX_DIR = join('/srv/praktomat/sandbox/', PRAKTOMAT_ID)
SANDBOX_DIR = join(UPLOAD_ROOT, "SolutionSandbox/")

ADMINS = [
  #('Praktomat', 'praktomat@ipd.info.uni-karlsruhe.de')
  ('Praktomat', 'praktomat@inf.h-brs.de')
]


#if MIRROR:
#	EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#	EMAIL_FILE_PATH = join(UPLOAD_ROOT, "sent-mails")
#else:
#	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#	EMAIL_HOST = "localhost"
#	EMAIL_PORT = 25
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "localhost"
EMAIL_PORT = 25


#DEFAULT_FROM_EMAIL = "praktomat@ipd.info.uni-karlsruhe.de"
DEFAULT_FROM_EMAIL = "praktomattest@inf.h-brs.de"

#DEBUG = MIRROR
DEBUG = False

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':   PRAKTOMAT_ID,
    }
}

# Private key used to sign uploded solution files in submission confirmation email
#PRIVATE_KEY = '/srv/praktomat/mailsign/signer_key.pem'
PRIVATE_KEY = None # '/home/praktomat/certificates/privkey.pem'

# Enable Shibboleth:
SHIB_ENABLED = False
REGISTRATION_POSSIBLE = False

ACCOUNT_CHANGE_POSSIBLE = False
DUMMY_MAT_NUMBERS = True
SHOW_CONTACT_LINK = False 


# LDAP
AUTHENTICATION_BACKENDS = (
    'accounts.ldap_auth.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LDAP_URI="ldap://ldap.inf.fh-brs.de"
LDAP_BASE="dc=fh-bonn-rhein-sieg,dc=de"




# Use a dedicated user to test submissions
USEPRAKTOMATTESTER = False

# Use docker to test submission
USESAFEDOCKER = True

# Various extra files and versions
#CHECKSTYLEALLJAR = '/srv/praktomat/contrib/checkstyle-5.7-all.jar'
CHECKSTYLEALLJAR = '/opt/praktomat-addons/checkstyle-6.15-all.jar'
JAVA_LIBS = { 'junit3' : '/usr/share/java/junit.jar', 'junit4' : '/opt/praktomat-addons/*' }
#JAVA_BINARY = 'javac-sun-1.7'
#JVM = 'java-sun-1.7'

# Our VM has 4 cores, so lets try to use them
# HBRS only 2 
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 2


# Finally load defaults for missing settings.
import defaults
defaults.load_defaults(globals())

