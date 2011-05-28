from django.contrib import admin
from praktomat.solutions.models import Solution, SolutionFile
from praktomat.checker.models import CheckerResult

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
	list_display = ["task", "author", "number", "creation_date", "final", "accepted", "warnings", "plagiarism"]
	list_filter = ["task", "author", "creation_date", "final", "accepted", "warnings", "plagiarism"]
	fieldsets = ((None, {
		  			'fields': ( "task", "author", "creation_date", ("final", "accepted", "warnings"), "plagiarism")
			  	}),)
	readonly_fields=["task", "author", "creation_date", "accepted", "final", "warnings"]
	inlines =  [CheckerResultInline, SolutionFileInline]
admin.site.register(Solution, SolutionAdmin)









