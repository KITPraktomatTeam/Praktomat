from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('praktomat.tasks.views',
	url(r'^$', 'taskList', name = 'task_list'),
	url(r'^preview$', 'taskPreview'),
	url(r'^(?P<task_id>\d+)/$', 'taskDetail', name='taskDetail'),
)

urlpatterns += patterns('praktomat.solutions.views',
	url(r'^(?P<task_id>\d+)/upload/$', 'solution_list', name='solution_list'),
	url(r'^(?P<task_id>\d+)/attestation/$', 'attestation', name='attestation'),
)