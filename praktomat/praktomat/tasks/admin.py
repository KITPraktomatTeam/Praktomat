from django.contrib import admin
from django.contrib.contenttypes import generic
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from praktomat.tasks.models import Task, MediaFile


from praktomat.checker.tests.AnonymityChecker import AnonymityCheckerInline
from praktomat.checker.tests.LineCounter import LineCounterInline
from praktomat.checker.tests.DiffChecker import DiffCheckerCheckerInline
from praktomat.checker.tests.InterfaceChecker import InterfaceCheckerInline
from praktomat.checker.tests.LineWidthChecker import LineWidthCheckerInline
from praktomat.checker.tests.TextChecker import TextCheckerInline
from praktomat.checker.tests.DejaGnu import DejaGnuSetupInline, DejaGnuTesterInline

from praktomat.checker.compiler.CXXBuilder import CXXBuilderInline
from praktomat.checker.compiler.CBuilder import CBuilderInline
from praktomat.checker.compiler.JavaBuilder import JavaBuilderInline

CheckerInlines = [	AnonymityCheckerInline,
					LineCounterInline,
					DiffCheckerCheckerInline,
					InterfaceCheckerInline, 
					LineWidthCheckerInline,
					TextCheckerInline,
					CBuilderInline,
					CXXBuilderInline,
					JavaBuilderInline,
					DejaGnuSetupInline,
					DejaGnuTesterInline,]

class MediaInline(admin.StackedInline): 
	model = MediaFile
	extra = 1

class TaskAdmin(admin.ModelAdmin):
	model = Task
	fieldsets = (
		(None, {
			'fields': ('title' , ('publication_date', 'submission_date'), 'description')
		}),
	)
	list_display = ('title','publication_date','submission_date')
	list_filter = ['publication_date']
	search_fields = ['title']
	date_hierarchy = 'publication_date'
	save_on_top = True
	inlines = [MediaInline] + CheckerInlines
	actions = ['export_tasks']
	
	def export_tasks(self, request, queryset):
		""" Export Task action """
		from django.http import HttpResponse
		response = HttpResponse(Task.export_Tasks(queryset).read(), mimetype="application/zip")
		response['Content-Disposition'] = 'attachment; filename=TaskExport.zip'
		self.message_user(request, "%s Task(s) was/were successfully exported." % len(queryset)) # will be shown on reload :(
		return response

#	def get_urls(self):
#		""" Add URL to task import """
#		urls = super(TaskAdmin, self).get_urls()
#		from django.conf.urls.defaults import patterns
#		my_urls = patterns('', (r'^import/$', 'tasks.views.import_tasks')) 
#		return my_urls + urls
	
	
	class Media:
		js = [	'static/script/jquery.js', 
				'static/jquery-ui.js', 
				'static/script/stacked_dynamic_inlines.js',
				#'static/script/dynamic_inlines_with_sort.js',
				
				'static/script/markitup/jquery.markitup.js',
				'static/script/markitup/sets/markdown/set.js',
				#'static/script/jquery.markitup.task.conf.js',
			]
		
		css = { 'all' : [ #'static/styles/dynamic_inlines_with_sort.css',
							'static/script/markitup/skins/simple/style.css',
							'static/script/markitup/sets/markdown/style.css',
						], }
						
		
		
	
admin.site.register(Task, TaskAdmin)


