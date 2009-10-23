from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('praktomat.solutions.views',
    url(r'^upload/$', 'upload_solution', name='praktomat.solutions.views.upload_solution'),
	url(r'^(?P<solution_id>\d+)/$', 'solution_detail', name='solution_detail'),
)



