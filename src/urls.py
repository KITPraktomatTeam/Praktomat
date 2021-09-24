from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
import sys
import os

import django.contrib.admindocs.urls
import tasks.views
import attestation.views
import solutions.views
import utilities.views
import accounts.urls
import tinymce.urls

from django.contrib import admin

urlpatterns = [
    # Index page
    url(r'^$', RedirectView.as_view(pattern_name='task_list', permanent=True), name="index"),

    # Admin
    url(r'^admin/tasks/task/(?P<task_id>\d+)/model_solution', tasks.views.model_solution, name="model_solution"),
    url(r'^admin/tasks/task/(?P<task_id>\d+)/final_solutions', tasks.views.download_final_solutions, name="download_final_solutions"),
    url(r'^admin/attestation/ratingscale/generate', attestation.views.generate_ratingscale, name="generate_ratingscale"),
    url(r'^admin/doc/', include(django.contrib.admindocs.urls)),
    url(r'^admin/', admin.site.urls),

    # Login and Registration
    url(r'^accounts/', include(accounts.urls)),

    # tinyMCE
    url(r'^tinymce/', include(tinymce.urls)),

    #Tasks
    url(r'^tasks/$', tasks.views.taskList, name = 'task_list'),
    url(r'^tasks/(?P<task_id>\d+)/$', tasks.views.taskDetail, name='task_detail'),

    # Solutions
    url(r'^solutions/(?P<solution_id>\d+)/$', solutions.views.solution_detail, name='solution_detail',kwargs={'full' : False}),
    url(r'^solutions/(?P<solution_id>\d+)/full/$', solutions.views.solution_detail, name='solution_detail_full', kwargs={'full': True}),
    url(r'^solutions/(?P<solution_id>\d+)/download$', solutions.views.solution_download, name='solution_download', kwargs={'include_checker_files' : False, 'include_artifacts' : False}),
    url(r'^solutions/(?P<solution_id>\d+)/download/artifacts/$', solutions.views.solution_download, name='solution_download_artifacts', kwargs={'include_checker_files' : False, 'include_artifacts' : True}),
    url(r'^solutions/(?P<solution_id>\d+)/download/full/$', solutions.views.solution_download, name='solution_download_full', kwargs={'include_checker_files' : True, 'include_artifacts' : True}),
    url(r'^solutions/(?P<solution_id>\d+)/run_checker$', solutions.views.solution_run_checker, name='solution_run_checker'),
    url(r'^tasks/(?P<task_id>\d+)/checkerresults/$', solutions.views.checker_result_list, name='checker_result_list'),
    url(r'^tasks/(?P<task_id>\d+)/solutiondownload$', solutions.views.solution_download_for_task, name='solution_download_for_task', kwargs={'include_checker_files' : False, 'include_artifacts' : False}),
    url(r'^tasks/(?P<task_id>\d+)/solutiondownload/artifacts/$', solutions.views.solution_download_for_task, name='solution_download_for_task_artifacts', kwargs={'include_checker_files' : False, 'include_artifacts' : True}),
    url(r'^tasks/(?P<task_id>\d+)/solutiondownload/full/$', solutions.views.solution_download_for_task, name='solution_download_for_task_full', kwargs={'include_checker_files' : True, 'include_artifacts' : True}),
    url(r'^tasks/(?P<task_id>\d+)/solutionupload/$', solutions.views.solution_list, name='solution_list'),
    url(r'^tasks/(?P<task_id>\d+)/solutionupload/user/(?P<user_id>\d+)$', solutions.views.solution_list, name='solution_list'),
    url(r'^tasks/(?P<task_id>\d+)/solutionupload/test/$', solutions.views.test_upload, name='upload_test_solution'),
    url(r'^tasks/(?P<task_id>\d+)/solutionupload/test/student/$', solutions.views.test_upload_student, name='upload_test_solution_student'),

    url(r'^tasks/(?P<task_id>\d+)/jplag$', solutions.views.jplag, name='solution_jplag'),

    #Attestation
    url(r'^tasks/(?P<task_id>\d+)/attestation/statistics$', attestation.views.statistics, name='statistics'),
    url(r'^tasks/(?P<task_id>\d+)/attestation/$', attestation.views.attestation_list, name='attestation_list'),
    url(r'^tasks/(?P<task_id>\d+)/attestation/new$', attestation.views.new_attestation_for_task, name='new_attestation_for_task'),
    url(r'^solutions/(?P<solution_id>\d+)/attestation/new$', attestation.views.new_attestation_for_solution, name='new_attestation_for_solution', kwargs={'force_create' : False}),
    url(r'^solutions/(?P<solution_id>\d+)/attestation/new/(?P<force_create>force_create)$', attestation.views.new_attestation_for_solution, name='new_attestation_for_solution'),
    url(r'^attestation/(?P<attestation_id>\d+)/edit$', attestation.views.edit_attestation, name='edit_attestation'),
    url(r'^attestation/(?P<attestation_id>\d+)/withdraw$', attestation.views.withdraw_attestation, name='withdraw_attestation'),
    url(r'^attestation/(?P<attestation_id>\d+)/run_checker', attestation.views.attestation_run_checker, name='attestation_run_checker'),
    url(r'^attestation/(?P<attestation_id>\d+)$', attestation.views.view_attestation, name='view_attestation'),
    url(r'^attestation/rating_overview$', attestation.views.rating_overview, name='rating_overview'),
    url(r'^attestation/rating_export.csv$', attestation.views.rating_export, name='rating_export'),

    url(r'^tutorial/$', attestation.views.tutorial_overview, name='tutorial_overview'),
    url(r'^tutorial/(?P<tutorial_id>\d+)$', attestation.views.tutorial_overview, name='tutorial_overview'),

    # Uploaded media
    url(r'^upload/(?P<path>SolutionArchive/Task_\d+/User_.*/Solution_(?P<solution_id>\d+)/.*)$', utilities.views.serve_solution_file),
    url(r'^upload/(?P<path>TaskMediaFiles.*)$', utilities.views.serve_unrestricted),
    url(r'^upload/(?P<path>TaskHtmlInjectorFiles.*)$', utilities.views.serve_staff_only),
    url(r'^upload/(?P<path>jplag.*)$', utilities.views.serve_staff_only, name='jplag_download'),
    url(r'^upload/(?P<path>CheckerFiles.*)$', utilities.views.serve_staff_only),
    url(r'^upload/(?P<path>.*)$', utilities.views.serve_access_denied),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
