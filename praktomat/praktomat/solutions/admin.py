from django.contrib import admin
from praktomat.solutions.models import Solution, SolutionFile
from praktomat.checker.models import CheckerResult

class CheckerResultInline(admin.TabularInline):
	model = CheckerResult
	extra = 0
	
class SolutionFileInline(admin.TabularInline):
	model = SolutionFile
	extra = 0

class SolutionAdmin(admin.ModelAdmin):
	model = Solution
	inlines =  [CheckerResultInline, SolutionFileInline]
admin.site.register(Solution, SolutionAdmin)









