from django.contrib import admin
from django.contrib.contenttypes import generic
from django.shortcuts import render_to_response
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.db import transaction
from tinymce.widgets import TinyMCE

from tasks.models import Task, MediaFile
from solutions.models import Solution, SolutionFile
from attestation.admin import RatingAdminInline

from checker.admin import CheckerInline

admin.autodiscover()

class MediaInline(admin.StackedInline): 
	model = MediaFile
	extra = 0

class TaskAdmin(admin.ModelAdmin):
	model = Task
	fieldsets = (
		(None, {
			'fields': ('title' , ('publication_date', 'submission_date'), 'description', ('supported_file_types', 'max_file_size'), 'final_grade_rating_scale')
		}),
	)
	list_display = ('title','publication_date','submission_date')
	list_filter = ['publication_date']
	search_fields = ['title']
	date_hierarchy = 'publication_date'
	save_on_top = True
	inlines = [MediaInline] + CheckerInline.__subclasses__() + [ RatingAdminInline]
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
		response = HttpResponse(Task.export_Tasks(queryset).read(), mimetype="application/zip")
		response['Content-Disposition'] = 'attachment; filename=TaskExport.zip'
		return response
		
	
	@transaction.autocommit
	def run_all_checkers(self, request, queryset):
		""" Rerun all checker including "not always" action """
		for task in queryset:
			task.check_all_final_solutions()
		self.message_user(request, "All final solutions were successfully checked.")

	def get_urls(self):
		""" Add URL to task import """
		urls = super(TaskAdmin, self).get_urls()
		from django.conf.urls.defaults import url, patterns
		my_urls = patterns('', url(r'^import/$', 'tasks.views.import_tasks', name='task_import')) 
		return my_urls + urls
	
admin.site.register(Task, TaskAdmin)


