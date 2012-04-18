from django.contrib import admin
from solutions.models import Solution, SolutionFile
from checker.models import CheckerResult
from django.conf import settings

class CheckerResultInline(admin.TabularInline):
	model = CheckerResult
	extra = 0
	can_delete = False
	fields = ["checker", "passed", "log"]
	readonly_fields = ["checker", "passed", "log"]
	
class SolutionFileInline(admin.TabularInline):
	model = SolutionFile
	extra = 0
	can_delete = False
	readonly_fields=["mime_type", "file"]


class SolutionAdmin(admin.ModelAdmin):
	model = Solution
	list_display = ["edit", "view_url", "download_url", "task", "author", "number", "creation_date", "final", "accepted", "warnings", "plagiarism"]
	list_filter = ["task", "author", "creation_date", "final", "accepted", "warnings", "plagiarism"]
	fieldsets = ((None, {
		  			'fields': ( "task", "author", "creation_date", ("final", "accepted", "warnings"), "plagiarism")
			  	}),)
	readonly_fields=["task", "author", "creation_date", "accepted", "final", "warnings"]
	inlines =  [CheckerResultInline, SolutionFileInline]

	def edit(self,solution):
		return 'Edit'
	edit.short_description = 'Edit (Admin Site)'

	def view_url(self,solution):
		return '<a href="%s%s">View</a>' % (settings.BASE_URL,'solutions/'+str(solution.id)+'/full/')
	view_url.allow_tags = True
	view_url.short_description = 'View (User Site)'

	def download_url(self,solution):
		return '<a href="%s%s">Download</a>' % (settings.BASE_URL,'solutions/'+str(solution.id)+'/download')
	download_url.allow_tags = True
	download_url.short_description = 'Download'

admin.site.register(Solution, SolutionAdmin)
	








