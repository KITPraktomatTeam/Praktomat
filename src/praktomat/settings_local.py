# -*- coding: utf-8 -*-
# settings which depend on the machine django runs on 

# This will show debug information in the browser if an exception occurs.
# Note that there are always going to be sections of your debug output that 
# are inappropriate for public consumption. File paths, configuration options, 
# and the like all give attackers extra information about your server.
# Never deploy a site into production with DEBUG turned on.
DEBUG = False

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

PRAKTOMAT_ID = 'praktomat_2011_SS'

# The URL where this site is reachable. 'http://localhost:8000/' in case of the developmentserver.
BASE_URL = 'https://praktomat.info.uni-karlsruhe.de/' + PRAKTOMAT_ID + '/'

# URL that serves the static media files (CSS, JavaScript and images) of praktomat contained in 'media/'.
# Make sure to use a trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = BASE_URL + 'media/'

# URL prefix for the administration site media (CSS, JavaScript and images) contained in the django package. 
# Make sure to use a trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = BASE_URL + 'media/admin/'

LOGIN_URL = BASE_URL + 'accounts/login/'
LOGIN_REDIRECT_URL = BASE_URL + 'tasks/'

# Absolute path to the directory that shall hold all uploaded files as well as files created at runtime.
# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = "/praktomatng/installations/" + PRAKTOMAT_ID + "/PraktomatSupport/"


ADMINS = (
		  # ('Your Name', 'your_email@domain.com'),
		  ('Praktomat', 'praktomat@ipd.info.uni-karlsruhe.de')
		  )


DATABASE_ENGINE = 'postgresql_psycopg2'   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'prog_ss11_aufgaben'  # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


# DEFAULT_FROM_EMAIL = ""
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = "praktomat"
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False

# Private key used to sign uploded solution files in submission confirmation email
PRIVATE_KEY = '/Users/danielkleinert/Documents/Arbeit/Praktomat/examples/certificates/privkey.pem'


MANAGERS = ADMINS

# The Compiler binarys used to compile a submitted solution
C_BINARY = 'gcc'
CXX_BINARY = 'c++'
JAVA_BINARY = 'javac'
JAVA_BINARY_SECURE = '/praktomat/bin/javac'
JAVA_GCC_BINARY = 'gcj'
JVM = 'java'
JVM_SECURE = '/praktomat/bin/java'
FORTRAN_BINARY = 'g77'
DEJAGNU_RUNTEST = '/usr/bin/runtest'
CHECKSTYLEALLJAR = '/praktomatng/checkstyle-all-4.4.jar'
JUNIT38='junit'

# Enable to run all scripts (checker) as the unix user 'praktomattester'. Therefore put 'praktomattester' as well
# as the Apache user '_www' (and your development user account) into a new group called praktomat. Also edit your
# sudoers file with "sudo visudo". Add the following lines to the end of the file to allow the execution of 
# commands with the user 'praktomattester' without requiring a password:
# "_www    		ALL=(praktomattester)NOPASSWD:ALL"
# "developer	ALL=(praktomattester)NOPASSWD:ALL"
USEPRAKTOMATTESTER = True


# Regular expression used to check the email domain of registering users.
EMAIL_VALIDATION_REGEX =  r".*@(student\.)?kit\.edu"

# Regular expression used to check the student number.
MAT_NUMBER_VALIDATION_REGEX = r"\d{5,7}"

# After this date no one can use the registration page anymore. Format: date(2005, 7, 14)
from datetime import date
DENY_REGISTRATION_FROM = date(2012, 01, 01)

# If enabled, the tutor can't see the name of the user, who subbmitted the solution.
ANONYMOUS_ATTESTATION = False
