# -*- coding: utf-8 -*-
# settings which depend on the machine django runs on 

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

# URL that serves the static media files (CSS, JavaScript and images) of praktomat contained in 'media/'.
# Make sure to use a trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost/media/'

# URL prefix for the administration site media (CSS, JavaScript and images) contained in the django package. 
# Make sure to use a trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Absolute path to the directory that shall hold all uploaded files as well as files created at runtime.
# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = "/Users/halluzinativ/Documents/Arbeit/PraktomatSupport/"

# URL that serves the uploaded files. 
# You need to configure the rights to download these in your webserver!
# Make sure to use a trailing slash if there is a path component (optional in other cases).
# Examples: "http://upload.lawrence.com", "http://example.com/upload/"
UPLOAD_URL = 'http://localhost/upload/'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Daniel Kleinert', 'herr.kleinert@googlemail.com')
)

#DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME ='praktomat'   # Or path to database file if using sqlite3.
#DATABASE_USER = 'postgres'             # Not used with sqlite3.
#DATABASE_PASSWORD = 'demo'         # Not used with sqlite3.
#DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

 
DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = UPLOAD_ROOT+'/Database'   # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


# DEFAULT_FROM_EMAIL = ""
EMAIL_HOST = "smtp.googlemail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "praktomat@googlemail.com"
EMAIL_HOST_PASSWORD = "baertram"
EMAIL_USE_TLS = True

MANAGERS = ADMINS

# The Compiler binarys used to compile a submitted solution
C_BINARY = 'gcc'
CXX_BINARY = 'c++'
JAVA_BINARY = 'javac'
JAVA_GCC_BINARY = 'gcj'
JVM = "java"
FORTRAN_BINARY = 'g77'
DEJAGNU_RUNTEST = '/opt/local/bin/runtest'
