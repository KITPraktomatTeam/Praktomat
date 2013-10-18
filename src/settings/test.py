# Settings for running the test-runner

from os.path import join, dirname

# The name that will be displayed on top of the page and in emails.
SITE_NAME = 'Praktomat Test instance'

# Identifie this Praktomat among multiple installation on one webserver
PRAKTOMAT_ID = 'test' 

# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# developmentserver.
BASE_HOST = 'http://localhost:8000'
BASE_PATH = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

UPLOAD_ROOT = "/tmp/does-not-exist"

SECRET_KEY = "not-so-secret"

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = UPLOAD_ROOT+'/Database'   # Or path to database file if using sqlite3.

PRIVATE_KEY = join(dirname(dirname(dirname(__file__))), 'examples', 'certificates', 'privkey.pem')

# Finally load defaults for missing setttings.
import defaults
defaults.load_defaults(globals())



