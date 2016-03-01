# Settings for development in the source tree

from os.path import join, dirname

# The name that will be displayed on top of the page and in emails.
SITE_NAME = 'Praktomat'

# Identifie this Praktomat among multiple installation on one webserver
PRAKTOMAT_ID = 'default' 

# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# developmentserver.
BASE_HOST = 'http://localhost:8000'
BASE_PATH = '/'

# URL to use when referring to static files.
STATIC_URL = BASE_PATH + 'static/'

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = join(dirname(dirname(dirname(__file__))),'data')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   UPLOAD_ROOT+'/Database',
    }
}


JPLAGJAR = join(dirname(dirname(dirname(__file__))), 'jplag.jar')

PRIVATE_KEY = join(dirname(dirname(dirname(__file__))), 'examples', 'certificates', 'privkey.pem')

# Finally load defaults for missing setttings.
import defaults
defaults.load_defaults(globals())

# To get exceptions logged as well:
MIDDLEWARE_CLASSES += (
        'utilities.exceptionlogger.ExceptionLoggingMiddleware',
    )
