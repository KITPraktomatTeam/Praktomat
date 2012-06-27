from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
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
	url(r'^admin/tasks/task/(?P<task_id>\d+)/model_solution', 'tasks.views.model_solution', name="model_solution"),
	url(r'^admin/tasks/task/(?P<task_id>\d+)/final_solutions', 'tasks.views.download_final_solutions', name="download_final_solutions"),
	url(r'^admin/attestation/ratingscale/generate', 'attestation.views.generate_ratingscale', name="generate_ratingscale"),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
	# Login and Registration
	(r'^accounts/', include('accounts.urls')),
	
	# tinyMCE 
	(r'^tinymce/', include('tinymce.urls')),
					   
	#Tasks
	url(r'^tasks/$', 'tasks.views.taskList', name = 'task_list'),
	url(r'^tasks/(?P<task_id>\d+)/$', 'tasks.views.taskDetail', name='task_detail'),

	# Solutions
	url(r'^solutions/(?P<solution_id>\d+)/$', 'solutions.views.solution_detail', name='solution_detail',kwargs={'full' : False}),
	url(r'^solutions/(?P<solution_id>\d+)/(?P<full>full)/$', 'solutions.views.solution_detail', name='solution_detail'),
   	url(r'^solutions/(?P<solution_id>\d+)/download$', 'solutions.views.solution_download', name='solution_download'),
	url(r'^solutions/(?P<solution_id>\d+)/run_checker$', 'solutions.views.solution_run_checker', name='solution_run_checker'),
	url(r'^tasks/(?P<task_id>\d+)/checkerresults/$', 'solutions.views.checker_result_list', name='checker_result_list'),
	url(r'^tasks/(?P<task_id>\d+)/solutiondownload$', 'solutions.views.solution_download_for_task', name='solution_download_for_task'),
	url(r'^tasks/(?P<task_id>\d+)/solutionupload/$', 'solutions.views.solution_list', name='solution_list'),
	url(r'^tasks/(?P<task_id>\d+)/solutionupload/user/(?P<user_id>\d+)$', 'solutions.views.solution_list', name='solution_list'),
					   
	#Attestation
	url(r'^tasks/(?P<task_id>\d+)/attestation/statistics$', 'attestation.views.statistics', name='statistics'),
	url(r'^tasks/(?P<task_id>\d+)/attestation/$', 'attestation.views.attestation_list', name='attestation_list'),
	url(r'^tasks/(?P<task_id>\d+)/attestation/new$', 'attestation.views.new_attestation_for_task', name='new_attestation_for_task'),
	url(r'^solutions/(?P<solution_id>\d+)/attestation/new$', 'attestation.views.new_attestation_for_solution', name='new_attestation_for_solution'),
	url(r'^attestation/(?P<attestation_id>\d+)/edit$', 'attestation.views.edit_attestation', name='edit_attestation'),
	url(r'^attestation/(?P<attestation_id>\d+)$', 'attestation.views.view_attestation', name='view_attestation'),
	url(r'^attestation/rating_overview$', 'attestation.views.rating_overview', name='rating_overview'),
	url(r'^attestation/rating_export.csv$', 'attestation.views.rating_export', name='rating_export'),
	
	url(r'^tutorial/$', 'attestation.views.tutorial_overview', name='tutorial_overview'),
   	url(r'^tutorial/(?P<tutorial_id>\d+)$', 'attestation.views.tutorial_overview', name='tutorial_overview'),
	
	# Uploaded media
	url(r'^upload/(?P<path>SolutionArchive/Task_\d+/User_.*/Solution_(?P<solution_id>\d+)/.*)$', 'utilities.views.serve_solution_file'),
	url(r'^upload/(?P<path>TaskMediaFiles.*)$', 'utilities.views.serve_unrestricted'),
	url(r'^upload/(?P<path>CheckerFiles.*)$', 'utilities.views.serve_staff_only'),
	url(r'^upload/(?P<path>.*)$', 'utilities.views.serve_access_denied'),
	
)


# only serve static files through django while in development - for safety and speediness
if 'runserver' in sys.argv or 'runserver_plus' in sys.argv or 'runconcurrentserver' in sys.argv: 
	media_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_path}),
        (r'^favicon.ico$', 'django.views.static.serve', {'document_root': media_path, 'path':"favicon.ico"}),
    )

