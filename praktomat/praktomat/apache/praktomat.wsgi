import os, sys
sys.path.append('/Users/halluzinativ/Documents')
sys.path.append('/Users/halluzinativ/Documents/praktomat')

os.environ['DJANGO_SETTINGS_MODULE'] = 'praktomat.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

