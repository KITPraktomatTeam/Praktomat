# Settings for development in the source tree

from os.path import join, dirname

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))

# The name that will be displayed on top of the page and in emails.
SITE_NAME = 'TestVM - Praktomat - devel'

# Identifie this Praktomat among multiple installation on one webserver
PRAKTOMAT_ID = 'devel' 

# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# developmentserver.
#BASE_HOST = 'http://praktomattest.inf.h-brs.de:8910'
BASE_HOST = 'http://localhost:8000'
BASE_PATH = '/' # + PRAKTOMAT_ID + '/'  # using here the PRAKTOMAT_ID  runserver and runserver_plus  don't manage it to let you login.

# URL to use when referring to static files.
STATIC_URL = BASE_PATH + 'static/'
STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
# UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "PraktomatSupport/")
# UPLOAD_ROOT = "/home/praktomat/inst/" + PRAKTOMAT_ID + "/work/"
#UPLOAD_ROOT = join(dirname(dirname(dirname(__file__))),'data')
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "debug-work/")


#SANDBOX_DIR = join('/srv/praktomat/sandbox/', PRAKTOMAT_ID)
#SANDBOX_DIR = join(UPLOAD_ROOT, "SolutionSandbox/")
#SANDBOX_DIR now defined in settings/defaults.py


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "praktomat_rhVM@inf.h-brs.de"

DEBUG = True

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

#overwrite to use the same settings from local.py
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
#sudo -u postgres createdb -O praktomat praktomat_devel

    

# SECRET_KEY gets generated via defaults.py

PRIVATE_KEY = join(dirname(dirname(dirname(__file__))), 'examples', 'certificates', 'privkey.pem')

#overwrite to use the same settings from local.py
PRIVATE_KEY = None

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

JPLAGJAR = join(dirname(dirname(dirname(__file__))), 'jplag.jar')
JPLAGJAR = '/opt/praktomat-addons/jplag.jar'

#CHECKSTYLEALLJAR = '/srv/praktomat/contrib/checkstyle-5.7-all.jar'
CHECKSTYLEALLJAR = '/opt/praktomat-addons/checkstyle-6.15-all.jar'
JAVA_LIBS = { 'junit3' : '/usr/share/java/junit.jar', 'junit4' : '/opt/praktomat-addons/*' }



# Our VM has 4 cores, so lets try to use them
# HBRS only 2
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 2


# Finally load defaults for missing settings.
import defaults
defaults.load_defaults(globals())

# To get exceptions logged as well:
MIDDLEWARE_CLASSES += (
        'utilities.exceptionlogger.ExceptionLoggingMiddleware',
    )
