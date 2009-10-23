import os, sys
 
# Calculate the path based on the location of the WSGI script.
# apache_configuration = os.path.dirname(__file__)
# project = os.path.dirname(apache_configuration)
# workspace = os.path.dirname(project)
# sys.path.append(workspace)
sys.path.append('/Users/halluzinativ/Documents/praktomat/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'praktomat.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
