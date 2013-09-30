# Settings for deployment

from os.path import join, dirname, basename
import re

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))

PRAKTOMAT_ID = basename(dirname(PRAKTOMAT_PATH))

match = re.match('praktomat_(\d+)_(WS|SS)(_Abschluss)?(_Mirror)?', PRAKTOMAT_ID)
if match:
	year = int(match.group(1))
	SITE_NAME = ''
	if match.group(3):
		SITE_NAME += "Abschlussaufgaben "
	SITE_NAME = 'Programmieren '
	if match.group(2) == "WS":
		SITE_NAME += "Wintersemester %d/%d" % (year, year+1)
	else:
		SITE_NAME += "Sommeremster %d" % year
	if match.group(4):
		SITE_NAME += " (Mirror)"
		MIRROR = True
	else:
		MIRROR = False
else:
	raise NotImplementedError("Autoconfig for PRAKTOMAT_ID %s not possible", PRAKTOMAT_ID)


# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# developmentserver.
BASE_HOST = 'https://praktomat.info.uni-karlsruhe.de'
BASE_PATH = '/' + PRAKTOMAT_ID + '/'

# URL to use when referring to static files.
STATIC_URL = BASE_PATH + 'static/'

STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = "/praktomatng/installations/" + PRAKTOMAT_ID + "/PraktomatSupport/"

ADMINS = [
  ('Praktomat', 'praktomat@ipd.info.uni-karlsruhe.de')
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = "praktomat@ipd.info.uni-karlsruhe.de"

EMAIL_HOST = "localhost"
if MIRROR:
	EMAIL_PORT = 4096
else:
	EMAIL_PORT = 25

DEBUG = MIRROR

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = PRAKTOMAT_ID

# Private key used to sign uploded solution files in submission confirmation email
PRIVATE_KEY = '/praktomatng/certificates/mailsign/signer_key.pem'

# Enable Shibboleth:
SHIB_ENABLED = True
REGISTRATION_POSSIBLE = False


# Finally load defaults for missing setttings.
import defaults
defaults.load_defaults(globals())

