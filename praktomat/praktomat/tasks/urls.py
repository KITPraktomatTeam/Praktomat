from django.conf.urls.defaults import *

urlpatterns = patterns('praktomat.tasks.views',
	url(r'^$', 'taskList', name = 'task_list'),
	url(r'^preview$', 'taskPreview'),
	url(r'^(?P<task_id>\d+)/$', 'taskDetail', name='taskDetail'),
)

urlpatterns += patterns('',
	url(r'^(?P<task_id>\d+)/solutionupload/$', 'praktomat.solutions.views.solution_list', name='solution_list'),
	url(r'^(?P<task_id>\d+)/attestation/', include('praktomat.attestation.urls')),
)