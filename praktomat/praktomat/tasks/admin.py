from django.contrib import admin
from django.contrib.contenttypes import generic
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
					InterfaceCheckerInline, # No Nested inlines in django as of yet. neds rewrite. :(
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
			'fields': ('title' , ('publication_date', 'submission_date'))
		}),
		('Nanana', {
		'description': 'lalala',
			'fields': ('description',)
		}),
	)
	list_display = ('title','publication_date','submission_date')
	list_filter = ['publication_date']
	search_fields = ['title']
	date_hierarchy = 'publication_date'
	save_on_top = True
	inlines = [MediaInline] + CheckerInlines
	
	class Media:
		js = [	'script/jquery.js', 
				'script/ui/ui.core.js', 
				'script/ui/ui.sortable.js', 
				'script/stacked_dynamic_inlines.js',
				#'script/dynamic_inlines_with_sort.js',
				'/script/markitup/jquery.markitup.js',
				'/script/markitup/sets/markdown/set.js',
			]
		
		css = { 'all' : [ #'styles/dynamic_inlines_with_sort.css',
							'/script/markitup/skins/simple/style.css',
							'/script/markitup/sets/markdown/style.css',
						], }
		
	
admin.site.register(Task, TaskAdmin)


