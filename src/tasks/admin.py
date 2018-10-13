# -*- coding: utf-8 -*-

from django.contrib import admin
from django.shortcuts import render
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.db import transaction
from django.core.urlresolvers import reverse
from tinymce.widgets import TinyMCE
from django.utils.html import format_html

from tasks.models import Task, MediaFile, HtmlInjector
from solutions.models import Solution, SolutionFile
from attestation.admin import RatingAdminInline

import tasks.views

from checker.admin import CheckerInline
from timeit import default_timer as timer

admin.autodiscover()

class MediaInline(admin.StackedInline): 
	model = MediaFile
	extra = 0

class HtmlInjectorInline(admin.StackedInline): 
	model = HtmlInjector
	extra = 0

class TaskAdmin(admin.ModelAdmin):
	model = Task
        readonly_fields = ('useful_links',)
	fieldsets = (
		(None, {
			'fields': (
                            'title',
                            ('publication_date', 'submission_date'),
                            'description',
                            ('supported_file_types', 'max_file_size'),
                            'final_grade_rating_scale',
                            'only_trainers_publish',
                            'warning_threshold',
                            'useful_links',
                        )
		}),
	)
	list_display = ('title','attestations_url','testupload_url','publication_date','submission_date','all_checker_finished')
	list_filter = ['publication_date']
	search_fields = ['title']
	date_hierarchy = 'publication_date'
	save_on_top = True
	inlines = [MediaInline] + [HtmlInjectorInline] + CheckerInline.__subclasses__() + [ RatingAdminInline]
	actions = ['export_tasks', 'run_all_checkers']
	
	formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

	class Media:
		js = (
				'frameworks/jquery/jquery.js',
				'frameworks/jquery/jquery-ui.js',
				'frameworks/jquery/jquery.tinysort.js',
				'script/checker-sort.js',
		)
	
	
	def export_tasks(self, request, queryset):
		""" Export Task action """
		from django.http import HttpResponse
		response = HttpResponse(Task.export_Tasks(queryset).read(), content_type="application/zip")
		response['Content-Disposition'] = 'attachment; filename=TaskExport.zip'
		return response
		
	
	def run_all_checkers(self, request, queryset):
		""" Rerun all checker including "not always" action """
		start = timer()
		count = 0
		for task in queryset:
			count += task.check_all_final_solutions()
		end = timer()
		self.message_user(request, "%d final solutions were successfully checked (%d seconds elapsed)." % (count, end-start))

	def get_urls(self):
		""" Add URL to task import """
		urls = super(TaskAdmin, self).get_urls()
		from django.conf.urls import url
		my_urls = [url(r'^import/$', tasks.views.import_tasks, name='task_import')]
		return my_urls + urls

        def attestations_url(self,task):
                return format_html ('<a href="{0}">Attestations (User site)</a>',
                    reverse('attestation_list', kwargs={'task_id': task.id}))
        attestations_url.allow_tags = True
        attestations_url.short_description = 'Attestations'

        def testupload_url(self,task):
                return format_html ('<a href="{0}">Test Submission</a>',
                    reverse('upload_test_solution', kwargs={'task_id': task.id}))
        testupload_url.allow_tags = True
        testupload_url.short_description = 'Test Submission'

        def useful_links(self, instance):
		if instance.id:
			return format_html (
			    '<a href="{0}">Attestations (including for-user-submission)</a> • ' +
			    '<a href="{1}">Test upload</a>',
			    reverse('attestation_list', kwargs={'task_id': instance.id}),
			    reverse('upload_test_solution', kwargs={'task_id': instance.id})
			    )
		else:
			return ""
        useful_links.allow_tags = True


admin.site.register(Task, TaskAdmin)


