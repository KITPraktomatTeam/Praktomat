from django.contrib import admin
from django.contrib.contenttypes import generic
from django.shortcuts import render_to_response
from django.contrib.auth.admin import UserAdmin
from django.db import models
from tinymce.widgets import TinyMCE

from praktomat.tasks.models import Task, MediaFile
from praktomat.solutions.models import Solution, SolutionFile
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

# Importing like that would be cleaner, but would result in bad ordering.
#from praktomat.checker.admin import CheckerInline
#CheckerInline.__subclasses__
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
	extra = 0

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
	inlines = [MediaInline] + CheckerInlines + [ RatingAdminInline]
	actions = ['export_tasks', 'run_all_checkers']
	
	formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
	
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
			if task.expired():
				task.all_checker_finished = True
				task.save()
		self.message_user(request, "%s solutions were successfully checked." % solution_count)

	def get_urls(self):
		""" Add URL to task import """
		urls = super(TaskAdmin, self).get_urls()
		from django.conf.urls.defaults import patterns
		my_urls = patterns('', (r'^import/$', 'praktomat.tasks.views.import_tasks')) 
		return my_urls + urls
	
admin.site.register(Task, TaskAdmin)


