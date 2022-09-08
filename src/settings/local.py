# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Settings for deployment

# These settings are KIT-specific and derive some parts of the settings
# from the directory name.
#
# If you are not deploying on praktomat.cs.kit.edu you need to rewrite this file.

from os.path import join, dirname, basename
import re

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))

PRAKTOMAT_ID = basename(dirname(PRAKTOMAT_PATH))

match = re.match(r'''
    (?:praktomat_)?
    (?P<algo1>algo1_)?
    (?P<cram>cram_)?
    (?P<birap>birap_)?
    (?P<tba>tba_)?
    (?P<mlfds>mlfds_)?
    (?P<pp>pp_)?
    (?P<iimb>iimb_)?
    (?P<year>\d+)_
    (?P<semester>WS|SS)
    (?P<abschluss>_Abschluss)?
    (?P<mirror>_Mirror)?
    ''', PRAKTOMAT_ID, flags=re.VERBOSE)

if match:
    if match.group('algo1') is not None:
        SITE_NAME = 'Algorithmen I '
    elif match.group('cram') is not None:
        SITE_NAME = 'CRAM '
    elif match.group('birap') is not None:
        SITE_NAME = 'BIRAP '
    elif match.group('mlfds') is not None:
        SITE_NAME = 'MLFDS '
    elif match.group('tba') is not None:
        SITE_NAME = 'Theorembeweiser '
    elif match.group('pp') is not None:
        SITE_NAME = 'Programmierparadigmen '
    elif match.group('iimb') is not None:
        SITE_NAME = 'Informatik im Maschinenbau '
    else:
        SITE_NAME = 'Programmieren '

    if match.group('abschluss'):
        SITE_NAME += "Abschlussaufgaben "

    year = int(match.group('year'))
    if match.group('semester') == "WS":
        SITE_NAME += "Wintersemester %d/%d" % (year, year+1)
    else:
        SITE_NAME += "Sommersemester %d" % year

    if match.group('mirror') is not None:
        SITE_NAME += " (Mirror)"
        MIRROR = True
    else:
        MIRROR = False

else:
    raise NotImplementedError("Autoconfig for PRAKTOMAT_ID %s not possible", PRAKTOMAT_ID)


# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# development server.
BASE_HOST = 'https://praktomat.cs.kit.edu'
BASE_PATH = '/' + PRAKTOMAT_ID + '/'

ALLOWED_HOSTS = [ 'praktomat.cs.kit.edu', ]

# URL to use when referring to static files.
# STATIC_URL = BASE_PATH + 'static/'
# STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")


# STATIC_URL now defined in settings/defaults.py
# STATIC_ROOT now defined in settings/defaults.py

TEST_MAXLOGSIZE=512

TEST_MAXFILESIZE=512

TEST_TIMEOUT=180

if "cram" in PRAKTOMAT_ID:
    TEST_TIMEOUT=600
    TEST_MAXMEM=200

if "birap" in PRAKTOMAT_ID:
    TEST_TIMEOUT=600

if "tba" in PRAKTOMAT_ID:
    TEST_TIMEOUT=600

if "Programmieren" in SITE_NAME or "Programmierung" in SITE_NAME:
    # Rating overview needs one POST parameter per student
    # and the default value (1000) might be too low
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000
    TEST_TIMEOUT=600

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "work-data/")


# SANDBOX_DIR now defined in settings/defaults.py

#if MIRROR:
#    SANDBOX_DIR = join('/srv/praktomat/sandbox_Mirror/', PRAKTOMAT_ID)
#else:
#    SANDBOX_DIR = join('/srv/praktomat/sandbox/', PRAKTOMAT_ID)

ADMINS = [
  ('Praktomat', 'praktomat@ipd.info.uni-karlsruhe.de')
]

SERVER_EMAIL = 'praktomat@i44vm3.info.uni-karlsruhe.de'


if MIRROR:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = join(UPLOAD_ROOT, "sent-mails")
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 25

DEFAULT_FROM_EMAIL = "praktomat@ipd.info.uni-karlsruhe.de"

DEBUG = MIRROR

#DATABASES = {
#    'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#            'NAME':   UPLOAD_ROOT+'/Database'+PRAKTOMAT_ID,
#    }
#}

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':   'praktomat_'+PRAKTOMAT_ID,
            'USER':   'the given username at database creation time',
            'PASSWORD':   'your given password at database creation time',
    }
}

# on linux command line  create database and databaseuser
#sudo -u postgres -P <db_user>
#sudo -u postgres -P praktomat
#
#sudo -u postgres createdb -O <db_user> <db_name>
#sudo -u postgres createdb -O praktomat praktomat_2017s

# SECRET_KEY gets generated via defaults.py

# Private key used to sign uploded solution files in submission confirmation email
PRIVATE_KEY = '/srv/praktomat/mailsign/signer_key.pem'
CERTIFICATE = '/srv/praktomat/mailsign/signer.pem'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Enable Shibboleth:
SHIB_ENABLED = True

# Set this to False to disable registration via the website, e.g. when Single Sign On is used
REGISTRATION_POSSIBLE = False


# If you use shibboleth identitiy provider, please have a look into defaults.py
# to see how to overwrite SHIB_ATTRIBUTE_MAP , SHIB_USERNAME , SHIB_PROVIDER




SYSADMIN_MOTD_URL = "https://praktomat.cs.kit.edu/sysadmin_motd.html"

# Use a dedicated user to test submissions
USEPRAKTOMATTESTER = False

# It is recomendet to use DOCKER and not a tester account
# for using Docker from https://github.com/nomeata/safe-docker
# Use docker to test submission
USESAFEDOCKER = True

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
# sudo chown praktomat:tester praktomat/src/checker/scripts/java
# sudo chown praktomat:tester praktomat/src/checker/scripts/javac
# sudo chmod u+x,g+x,o-x praktomat/src/checker/scripts/java
# sudo chmod u+x,g+x,o-x praktomat/src/checker/scripts/javac




# Does Apache use "mod_xsendfile" version 1.0?
# If you use "libapache2-mod-xsendfile", this flag needs to be set to False
MOD_XSENDFILE_V1_0 = True

# Our VM has 4 cores, so lets try to use them
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 6
# But not with Isabelle, which is memory bound
if match and match.group('tba') is not None:
    NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 1



# Various extra files and versions

JPLAGJAR = join(dirname(dirname(dirname(__file__))), 'jplag.jar')
JPLAGJAR = '/opt/praktomat-addons/jplag.jar'

CHECKSTYLEALLJAR = '/srv/praktomat/contrib/checkstyle-5.7-all.jar'
CHECKSTYLEALLJAR = '/opt/praktomat-addons/checkstyle-6.15-all.jar'
CHECKSTYLEALLJAR = '/opt/praktomat-addons/ws2020/checkstyle-8.14-all.jar'

LANG = "en_US.UTF-8"
LANGUAGE = "en_US:en"

# Finally load defaults for missing settings.
from . import defaults
defaults.load_defaults(globals())
