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
PRAKTOMAT_ID = '2016w' 
	(?P<tba>tba_)?
	(?P<mlfds>mlfds_)?
	elif match.group('mlfds') is not None:
		SITE_NAME = 'MLFDS '
	elif match.group('tba') is not None:
		SITE_NAME = 'Theorembeweiser '


# The name that will be displayed on top of the page and in emails.
SITE_NAME = 'TestVM - Praktomat - local'



# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# developmentserver.
#BASE_HOST = 'https://praktomat.cs.kit.edu'
BASE_HOST = 'https://localhost/'
BASE_PATH = '/' + PRAKTOMAT_ID + '/'

#ALLOWED_HOSTS = [ 'praktomat.cs.kit.edu', ]
#ALLOWED_HOSTS = [ 'praktomattest.inf.h-brs.de', ]
ALLOWED_HOSTS = [ 'localhost', ]

# URL to use when referring to static files.
STATIC_URL = BASE_PATH + 'static/'
STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")

#if "cram" in PRAKTOMAT_ID:
#  TEST_TIMEOUT=600

if "tba" in PRAKTOMAT_ID:
  TEST_TIMEOUT=600

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
# UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "PraktomatSupport/")
# UPLOAD_ROOT = "/home/praktomat/inst/" + PRAKTOMAT_ID + "/work/"
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "work/")


#SANDBOX_DIR = join('/srv/praktomat/sandbox/', PRAKTOMAT_ID)
#SANDBOX_DIR = join(UPLOAD_ROOT, "SolutionSandbox/")
#SANDBOX_DIR now defined in settings/defaults.py

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




# Old Comments ... I like them to keep
#Configuration for PostGreSQL
#DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = 'Praktomat'   # Or path to database file if using sqlite3.
#DATABASE_USER = 'postgres'    # Not used with sqlite3.
#DATABASE_PASSWORD = 'postgres'# Not used with sqlite3.
#DATABASE_HOST = 'localhost'   # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = '5432'        # Set to empty string for default. Not used with sqlite3.

#Configuration for SQLite
#DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = UPLOAD_ROOT+'/Database'   # Or path to database file if using sqlite3.
#DATABASE_USER = ''             # Not used with sqlite3.
#DATABASE_PASSWORD = ''         # Not used with sqlite3.
#DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   UPLOAD_ROOT+'/Database'+PRAKTOMAT_ID,
    }
}

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':   'praktomat_'+PRAKTOMAT_ID,
            'USER':   'praktomat',
            'PASSWORD':   'praktomat',
    }
}
# on linux command line  create database and databaseuser 
#sudo -u postgres -P <db_user>
#sudo -u postgres -P praktomat
#
#sudo -u postgres createdb -O <db_user> <db_name>
#sudo -u postgres createdb -O praktomat praktomat_2016w


# SECRET_KEY gets generated via defaults.py

# Private key used to sign uploded solution files in submission confirmation email
#PRIVATE_KEY = '/srv/praktomat/mailsign/signer_key.pem'
PRIVATE_KEY = None # '/home/praktomat/certificates/privkey.pem'

# Enable Shibboleth:
SHIB_ENABLED = False

# Set this to False to disable registration via the website, e.g. when Single Sign On is used
REGISTRATION_POSSIBLE = False

# If you use shibboleth identitiy provider, please have a look into defaults.py 
# to see how to overwrite SHIB_ATTRIBUTE_MAP , SHIB_USERNAME , SHIB_PROVIDER 

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




# Use a dedicated user "tester" to test submissions
USEPRAKTOMATTESTER = True

# It is recomendet to use DOCKER and not a tester account
# for using Docker from https://github.com/nomeata/safe-docker
# Use docker to test submission
USESAFEDOCKER = False

# Linux User "tester" and Usergroup "praktomat"
# Enable to run all scripts (checker) as the unix user 'tester'. 
# Therefore put 'tester' as well as the Apache user '_www' (and your development user account) 
# into a new group called "praktomat". 

# Also edit your sudoers file with "sudo visudo -f /etc/sudoers.d/praktomat-tester". 
# Add the following lines to the end of the file to allow the execution of 
# commands with the user 'tester' without requiring a password:
# "_www		ALL=(tester) NOPASSWD: ALL"
# "developer	ALL=(tester) NOPASSWD: ALL"

# Add the following lines to the end of the file 
# to allow user Praktomat the execution of scriptfile  safe-docker  without requiring a password:
# "praktomat	ALL= NOPASSWD: /usr/local/bin/safe-docker"

# If you want to switch between "testuser" and "Docker" 
# use "sudo visudo -f /etc/sudoers.d/praktomat-tester"
# "_www		ALL=(tester) NOPASSWD: ALL"
# "developer	ALL=(tester) NOPASSWD: ALL"
# "praktomat 	ALL=(tester) NOPASSWD: ALL, NOPASSWD: /usr/local/bin/safe-docker"
#
# be shure that you change file permission 
# sudo chown praktomat:tester praktomat/src/checker/scripts/java
# sudo chown praktomat:tester praktomat/src/checker/scripts/javac
# sudo chmod u+x,g+x,o-x praktomat/src/checker/scripts/java
# sudo chmod u+x,g+x,o-x praktomat/src/checker/scripts/javac 




# Various extra files and versions
JPLAGJAR = '/srv/praktomat/contrib/jplag.jar'
JPLAGJAR = '/opt/praktomat-addons/jplag.jar'

#CHECKSTYLEALLJAR = '/srv/praktomat/contrib/checkstyle-5.7-all.jar'
CHECKSTYLEALLJAR = '/opt/praktomat-addons/checkstyle-6.15-all.jar'

JAVA_LIBS = { 'junit3' : '/usr/share/java/junit.jar', 'junit4' : '/opt/praktomat-addons/*' }
#JAVA_BINARY = 'javac-sun-1.7'
#JVM = 'java-sun-1.7'

# Our VM has 4 cores, so lets try to use them
# NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 6
# HBRS only 2 
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 2
# But not with Isabelle, which is memory bound
if match.group('tba') is not None:
    NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 1

# Finally load defaults for missing settings.
import defaults
defaults.load_defaults(globals())

