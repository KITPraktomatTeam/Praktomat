# -*- coding: utf-8 -*-
# settings which depend on the machine django runs on 

from os.path import dirname, join

# This will show debug information in the browser if an exception occurs.
# Note that there are always going to be sections of your debug output that 
# are inappropriate for public consumption. File paths, configuration options, 
# and the like all give attackers extra information about your server.
# Never deploy a site into production with DEBUG turned on.
DEBUG = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# The name that will be displayed on top of the page and in emails.
SITE_NAME = 'Praktomat'

# Identifie this Praktomat among multiple installation on one webserver
PRAKTOMAT_ID = 'default' 

# The URL where this site is reachable. 'http://localhost:8000/' in case of the developmentserver.
BASE_URL = 'http://localhost:8000/'  + PRAKTOMAT_ID + '/' 

# URL that serves the static media files (CSS, JavaScript and images) of praktomat contained in 'media/'.
# Make sure to use a trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = BASE_URL + 'media/'

# URL prefix for the administration site media (CSS, JavaScript and images) contained in the django package. 
# Make sure to use a trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = BASE_URL + 'media/admin/'


SESSION_COOKIE_PATH = '/' + PRAKTOMAT_ID + '/'
CSRF_COOKIE_NAME = 'csrftoken_' + PRAKTOMAT_ID

# Absolute path to the directory that shall hold all uploaded files as well as files created at runtime.
# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = "/home/praktomat/installations/" + PRAKTOMAT_ID + "/PraktomatSupport/"


# Absolute path to the praktomat source
PRAKTOMAT_ROOT = dirname(dirname(__file__))


ADMINS = [
		  # ('Your Name', 'your_email@domain.com'),
		  ('Daniel Kleinert', 'herr.kleinert@googlemail.com')
		  ]

#DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME ='praktomat'   # Or path to database file if using sqlite3.
#DATABASE_USER = 'postgres'             # Not used with sqlite3.
#DATABASE_PASSWORD = 'demo'         # Not used with sqlite3.
#DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


#DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = 'Praktomat'   # Or path to database file if using sqlite3.
#DATABASE_USER = 'postgres'             # Not used with sqlite3.
#DATABASE_PASSWORD = 'postgres'         # Not used with sqlite3.
#DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = '5432'             # Set to empty string for default. Not used with sqlite3.

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = UPLOAD_ROOT+'/Database'   # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DEFAULT_FROM_EMAIL = ""
EMAIL_HOST = "smtp.googlemail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "praktomat@googlemail.com"
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True

# Private key used to sign uploded solution files in submission confirmation email
PRIVATE_KEY = '/home/praktomat/certificates/privkey.pem'

MANAGERS = ADMINS

# The Compiler binarys used to compile a submitted solution
C_BINARY = 'gcc'
CXX_BINARY = 'c++'
JAVA_BINARY = 'javac'
JAVA_BINARY_SECURE = PRAKTOMAT_ROOT + '/src/checker/scripts/javac'
JAVA_GCC_BINARY = 'gcj'
JVM = 'java'
JVM_SECURE = PRAKTOMAT_ROOT + '/src/checker/scripts/java'
FORTRAN_BINARY = 'g77'
DEJAGNU_RUNTEST = '/usr/bin/runtest'
CHECKSTYLEALLJAR = '/home/praktomat/contrib/checkstyle-all-4.4.jar'
JUNIT38='junit'
JAVA_LIBS = { 'junit3' : '/usr/share/java/junit.jar', 'junit4' : '/usr/share/java/junit4.jar' }
JCFDUMP='jcf-dump'


# Enable to run all scripts (checker) as the unix user 'tester'. Therefore put 'tester' as well
# as the Apache user '_www' (and your development user account) into a new group called praktomat. Also edit your
# sudoers file with "sudo visudo". Add the following lines to the end of the file to allow the execution of 
# commands with the user 'tester' without requiring a password:
# "_www    		ALL=(tester)NOPASSWD:ALL"
# "developer	ALL=(tester)NOPASSWD:ALL"
USEPRAKTOMATTESTER = False


# This enables Shibboleth-Support.
# In order to actually get it working, you need to protec the location
# .../accounts/shib_login in the apache configuration, e.g. with this stanca:
#	<Location /shibtest/accounts/shib_login>
#		Order deny,allow
#		AuthType shibboleth
#		ShibRequireSession On
#		Require valid-user
#	</Location>
#
# You probably want to disable REGISTRATION_POSSIBLE if you enable Shibboleth
# support

SHIB_ENABLED = True

SHIB_ATTRIBUTE_MAP = {
	"mail": (True, "email"),
	"givenName": (True, "first_name"),
	"sn": (True, "last_name"),
	"matriculationNumber": (True, "matriculationNumber"),
}

SHIB_USERNAME = "email"

# This is shown as the name of the identitiy provider on the welcome page
SHIB_PROVIDER = "kit.edu"

# Set this to False to disable registration via the website, e.g. when Single Sign On is used
REGISTRATION_POSSIBLE = False

# Length of timeout applied whenever an external check that runs a students submission is executed,
# for example: JUnitChecker, DejaGnuChecker
TEST_TIMEOUT=30

# Maximal size (in kbyte) of files created whenever an external check that runs a students submission is executed,
# for example: JUnitChecker, DejaGnuChecker
TEST_MAXFILESIZE=64

# Maximal size (in kbyte) of checker logs accepted. This setting is respected currently only by:
# JUnitChecker, ScriptChecker, 
TEST_MAXLOGSIZE=64
