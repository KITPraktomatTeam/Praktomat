from django.contrib import admin
from django.contrib.contenttypes import generic
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from praktomat.tasks.models import Task, MediaFile
from praktomat.attestation.admin import RatingAdminInline


from praktomat.checker.tests.AnonymityChecker import AnonymityCheckerInline
from praktomat.checker.tests.LineCounter import LineCounterInline
from praktomat.checker.tests.DiffChecker import DiffCheckerInline
from praktomat.checker.tests.CreateFileChecker import CreateFileCheckerInline
from praktomat.checker.tests.ScriptChecker import ScriptCheckerInline
from praktomat.checker.tests.InterfaceChecker import InterfaceCheckerInline
from praktomat.checker.tests.LineWidthChecker import LineWidthCheckerInline
from praktomat.checker.tests.TextChecker import TextCheckerInline
from praktomat.checker.tests.DejaGnu import DejaGnuSetupInline, DejaGnuTesterInline

from praktomat.checker.compiler.CXXBuilder import CXXBuilderInline
from praktomat.checker.compiler.CBuilder import CBuilderInline
from praktomat.checker.compiler.JavaBuilder import JavaBuilderInline
from praktomat.checker.compiler.JavaGCCBuilder import JavaGCCBuilderInline
from praktomat.checker.compiler.FortranBuilder import FortranBuilderInline

CheckerInlines = [	AnonymityCheckerInline,
					LineCounterInline,
					CreateFileCheckerInline,
					DiffCheckerInline,
					ScriptCheckerInline,
					InterfaceCheckerInline, 
					LineWidthCheckerInline,
					TextCheckerInline,
					CBuilderInline,
					CXXBuilderInline,
					JavaBuilderInline,
					JavaGCCBuilderInline,
					FortranBuilderInline,
					DejaGnuSetupInline,
					DejaGnuTesterInline,]

admin.autodiscover()

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
	inlines = [MediaInline] + CheckerInlines + [RatingAdminInline]
	actions = ['export_tasks', 'run_all_checkers']
	
	def export_tasks(self, request, queryset):
		""" Export Task action """
		from django.http import HttpResponse
		response = HttpResponse(Task.export_Tasks(queryset).read(), mimetype="application/zip")
		response['Content-Disposition'] = 'attachment; filename=TaskExport.zip'
		return response
		
	def run_all_checkers(self, request, queryset):
		""" Rerun all checker including "not always" action """
		solution_count = 0
		for task in queryset:
			for solution in task.solution_set.all():
				solution.check(True)
				solution_count += 1
		self.message_user(request, "%s solutions were successfully checked." % solution_count)


	def get_urls(self):
		""" Add URL to task import """
		urls = super(TaskAdmin, self).get_urls()
		from django.conf.urls.defaults import patterns
		my_urls = patterns('', (r'^import/$', 'tasks.views.import_tasks')) 
		return my_urls + urls
	
	
	class Media:
		js = [	'static/script/jquery.js', 
				'static/script/jquery-ui.js', 
				'static/script/stacked_dynamic_inlines.js',
				#'static/script/dynamic_inlines_with_sort.js',
				
				'static/script/tiny_mce/jquery.tinymce.js',
				'static/script/syntaxhighlighter/scripts/shCore.js',
				'static/script/syntaxhighlighter/scripts/shBrushPython.js',
				'static/script/taskadmin.js',
			]
		
		css = { 'all' : [	'static/script/syntaxhighlighter/styles/shCore.css', # Doesn't work
							'static/script/syntaxhighlighter/styles/shThemeEclipse.css',
							#'static/styles/dynamic_inlines_with_sort.css',
						], }
						
		
		
	
admin.site.register(Task, TaskAdmin)


