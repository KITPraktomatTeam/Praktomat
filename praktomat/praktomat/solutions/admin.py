from django.contrib import admin
from praktomat.solutions.models import Solution
from praktomat.checker.models import CheckerResult

class CheckerResultInline(admin.TabularInline):
	model = CheckerResult
	extra = 0

class SolutionAdmin(admin.ModelAdmin):
	model = Solution
	inlines =  [CheckerResultInline]
admin.site.register(Solution, SolutionAdmin)









