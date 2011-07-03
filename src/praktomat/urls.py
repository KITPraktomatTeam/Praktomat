from django.conf.urls.defaults import *
from django.conf import settings
from django.core.urlresolvers import reverse
import sys
import os

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Index page
	url(r'^$', 'django.views.generic.simple.redirect_to', {'url': 'tasks/'}, name="index"),
	
	# Admin
	url(r'^admin/tasks/task/(?P<task_id>\d+)/model_solution', 'praktomat.tasks.views.model_solution', name="model_solution"),
	url(r'^admin/tasks/task/(?P<task_id>\d+)/final_solutions', 'praktomat.tasks.views.download_final_solutions', name="download_final_solutions"),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
	url(r'^admin/$', admin.site.root, name="admin"), # allows for url admin
    
	# Login and Registration
	(r'^accounts/', include('praktomat.accounts.urls')),
	
	# tinyMCE 
	(r'^tinymce/', include('tinymce.urls')),
	
	#Tasks
	url(r'^tasks/$', 'praktomat.tasks.views.taskList', name = 'task_list'),
	url(r'^tasks/(?P<task_id>\d+)/$', 'praktomat.tasks.views.taskDetail', name='task_detail'),

	# Solutions
	url(r'^solutions/(?P<solution_id>\d+)/$', 'praktomat.solutions.views.solution_detail', name='solution_detail'),
	url(r'^tasks/(?P<task_id>\d+)/solutionupload/$', 'praktomat.solutions.views.solution_list', name='solution_list'),
	url(r'^tasks/(?P<task_id>\d+)/solutionupload/user/(?P<user_id>\d+)$', 'praktomat.solutions.views.solution_list', name='solution_list'),
					   
	#Attestation
	url(r'^tasks/(?P<task_id>\d+)/attestation/statistics$', 'praktomat.attestation.views.statistics', name='statistics'),
	url(r'^tasks/(?P<task_id>\d+)/attestation/$', 'praktomat.attestation.views.attestation_list', name='attestation_list'),
	url(r'^tasks/(?P<task_id>\d+)/attestation/new$', 'praktomat.attestation.views.new_attestation', name='new_attestation'),
	url(r'^attestation/(?P<attestation_id>\d+)/edit$', 'praktomat.attestation.views.edit_attestation', name='edit_attestation'),
	url(r'^attestation/(?P<attestation_id>\d+)$', 'praktomat.attestation.views.view_attestation', name='view_attestation'),
	url(r'^attestation/rating_overview$', 'praktomat.attestation.views.rating_overview', name='rating_overview'),
	url(r'^attestation/rating_export.csv$', 'praktomat.attestation.views.rating_export', name='rating_export'),
	
	# Uploaded media
	url(r'^upload/(?P<path>SolutionArchive/Task_\d+/User_.*/Solution_(?P<solution_id>\d+)/.*)$', 'praktomat.utilities.views.serve_solution_file'),
	url(r'^upload/(?P<path>TaskMediaFiles.*)$', 'praktomat.utilities.views.serve_unrestricted'),
	url(r'^upload/(?P<path>CheckerFiles.*)$', 'praktomat.utilities.views.serve_staff_only'),
	url(r'^upload/(?P<path>.*)$', 'praktomat.utilities.views.serve_access_denied'),
	
)



# only serve static files through django while in development - for safety and speediness
if 'runserver' in sys.argv or 'runserver_plus' in sys.argv or 'runconcurrentserver' in sys.argv: 
	media_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'media')
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_path}),
        (r'^favicon.ico$', 'django.views.static.serve', {'document_root': media_path, 'path':"favicon.ico"}),
    )

