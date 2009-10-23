from django.conf.urls.defaults import *
from django.conf import settings
from django.core.urlresolvers import reverse
import sys

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^praktomat/', include('praktomat.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/(.*)', admin.site.root),
	url(r'^admin/$', admin.site.root, name="admin"), # allows for url admin
    
	# Login and Registration
	(r'^accounts/', include('praktomat.accounts.urls')),
	
    # Index page
	url(r'^$', 'django.views.generic.simple.redirect_to', {'url': 'tasks/'}, name="index"),

    (r'^tasks/', include('praktomat.tasks.urls')),
	(r'^solutions/', include('praktomat.solutions.urls')),
)

# only serve static files through django while in development - for safety and speediness
if 'runserver' in sys.argv or 'runserver_plus' in sys.argv: 
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^favicon.ico$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'path':"favicon.ico"}),
    )
    
