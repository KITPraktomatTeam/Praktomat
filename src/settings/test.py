# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Settings for running the test-runner

import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )


from os.path import join, dirname

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))

# The name that will be displayed on top of the page and in emails.
SITE_NAME = 'Praktomat Test instance - some non ascii literals - ä ü ö ß'

# Identify this Praktomat among multiple installations on one webserver
PRAKTOMAT_ID = 'test'

# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# development server.
BASE_HOST = 'http://localhost:8000'
BASE_PATH = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

UPLOAD_ROOT = join(dirname(dirname(dirname(__file__))), 'data')
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "test-data/")

SECRET_KEY = "not-so-secret"

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   UPLOAD_ROOT+'/DjangoTestDatabase'+PRAKTOMAT_ID,
    }
}

DEBUG = False

PRIVATE_KEY = join(dirname(dirname(dirname(__file__))), 'examples', 'certificates', 'privkey.pem')
CERTIFICATE = join(dirname(dirname(dirname(__file__))), 'examples', 'certificates', 'signer.pem')

LANG = "en_US.UTF-8"
LANGUAGE = "en_US:en"

# Finally load defaults for missing settings.
from . import defaults
defaults.load_defaults(globals())
