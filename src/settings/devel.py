# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Settings for development in the source tree

from os.path import join, dirname

# set Debug mode True or False; in development version should be True
DEBUG = True

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))

# The name that will be displayed on top of the page and in emails.
SITE_NAME = u'Development Praktomat- some non ascii letters in site name: ä ü ö ß'

# Identifie this Praktomat among multiple installation on one webserver
PRAKTOMAT_ID = '2021t'

# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# developmentserver.
BASE_HOST = 'http://localhost:8000'
BASE_PATH = '/' # + PRAKTOMAT_ID + '/'  # using here the PRAKTOMAT_ID  runserver and runserver_plus  don't manage it to let you login.
ALLOWED_HOSTS = [
 # You can add a FQDN-of your Dev-Server here ...
 #'praktomat.local',
 '.localhost',
 '127.0.0.1',
 '[::1]']


# URL to use when referring to static files.
# static files are collecting outside of Praktomat root-folder
#STATIC_URL now defined in settings/defaults.py
#STATIC_ROOT now defined in settings/defaults.py
# If you want to collect static files inside Praktomat-root-folder while developing, activate next line
# STATIC_URL = BASE_PATH + 'static/'


# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = join(dirname(dirname(dirname(__file__))), 'data')
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "debug-data/")


#if you change SANDBOX_DIR you must change path informations in files of Praktomat/src/checker/scripts/*
#SANDBOX_DIR now defined in settings/defaults.py

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = "localhost"
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "praktomat_devel@localhost.local"




DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   UPLOAD_ROOT+'/Database'+PRAKTOMAT_ID,
    }
}

#overwrite to use the same settings from local.py
#DATABASES = {
#    'default': {
#            'ENGINE': 'django.db.backends.postgresql_psycopg2',
#            'NAME':   'praktomat_'+PRAKTOMAT_ID,
#            'USER':   'the given username at database creation time',
#            'PASSWORD':   'your given password at database creation time',
#    }
#}

# on linux command line  create database and databaseuser
#sudo -u postgres -P <db_user>
#sudo -u postgres -P praktomat
#
#sudo -u postgres createdb -O <db_user> <db_name>
#sudo -u postgres createdb -O praktomat praktomat_devel


PRIVATE_KEY = join(dirname(dirname(dirname(__file__))), 'examples', 'certificates', 'privkey.pem')
CERTIFICATE = join(dirname(dirname(dirname(__file__))), 'examples', 'certificates', 'signer.pem')

#overwrite to use the same settings from local.py
PRIVATE_KEY = None

# Enable Shibboleth:
SHIB_ENABLED = False

# Set this to False to disable registration via the website, e.g. when Single Sign On is used
REGISTRATION_POSSIBLE = False

# If you use shibboleth identitiy provider, please have a look into defaults.py
# to see how to overwrite SHIB_ATTRIBUTE_MAP , SHIB_USERNAME , SHIB_PROVIDER




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
# be sure that you change file permission
# sudo chown praktomat:tester Praktomat/src/checker/scripts/java
# sudo chown praktomat:tester Praktomat/src/checker/scripts/javac
# sudo chmod u+x,g+x,o-x Praktomat/src/checker/scripts/java
# sudo chmod u+x,g+x,o-x Praktomat/src/checker/scripts/javac


# Our VM has 4 cores, so lets try to use them
# HBRS only 2 on development-VM but 4 on praktomattest and praktomat
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 2



# Various extra files and versions

JPLAGJAR = join(dirname(dirname(dirname(__file__))), 'jplag.jar')
JPLAGJAR = '/opt/praktomat-addons/jplag.jar'

#CHECKSTYLEALLJAR = '/srv/praktomat/contrib/checkstyle-5.7-all.jar'
CHECKSTYLEALLJAR = '/opt/praktomat-addons/checkstyle-6.15-all.jar'
JAVA_LIBS = { 'junit3' : '/usr/share/java/junit.jar', 'junit4' : '/opt/praktomat-addons/*' }

LANG = "en_US.UTF-8"
LANGUAGE = "en_US:en"

# Finally load defaults for missing settings.
from . import defaults
defaults.load_defaults(globals())

# To get exceptions logged as well:
MIDDLEWARE += [
        'utilities.exceptionlogger.ExceptionLoggingMiddleware',
    ]
