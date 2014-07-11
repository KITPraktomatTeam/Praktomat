# -*- coding: utf-8 -*-

from django.contrib import admin
from solutions.models import Solution, SolutionFile
from checker.models import CheckerResult
from checker.models import check_multiple
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Max
from django.utils.html import format_html



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
	list_display = ["edit", "view_url", "download_url", "run_checker_url", "task", "show_author", "number", "creation_date", "final", "accepted", "warnings", "latest_of_only_failed", "plagiarism"]
	list_filter = ["task", "author", "creation_date", "final", "accepted", "warnings", "plagiarism"]
	fieldsets = ((None, {
		  			'fields': ( "task", "show_author", "creation_date", ("final", "accepted", "warnings"), "plagiarism",'useful_links')
			  	}),)
	readonly_fields=["task", "show_author", "creation_date", "accepted", "final", "warnings",'useful_links']
	inlines =  [CheckerResultInline, SolutionFileInline]
	actions = ['run_checkers','run_checkers_all']

	def run_checkers_all(self, request, queryset):
		""" Run Checkers (including those not run at submission) for selected solution """
		check_multiple(queryset,True)
		self.message_user(request, "Checkers (including those not run at submission) for selected solutions were successfully run.")

	run_checkers_all.short_description = "Run Checkers (including those not run at submission) for selected solution "


	def run_checkers(self, request, queryset):
		""" Run Checkers (only those also run at submission) for selected solutions"""
		check_multiple(queryset,False)
		self.message_user(request, "Checkers (only those also run at submission) for selected solutions were successfully run.")

	run_checkers.short_description = " Run Checkers (only those also run at submission) for selected solutions"
		

	def edit(self,solution):
		return 'Edit'
	edit.short_description = 'Edit (Admin Site)'

	def view_url(self,solution):
		return '<a href="%s">View</a>' % (reverse('solution_detail', args=[solution.id])+'full/')
	view_url.allow_tags = True
	view_url.short_description = 'View (User Site)'

	def download_url(self,solution):
		return '<a href="%s">Download</a>' % (reverse('solution_download', args=[solution.id]))
	download_url.allow_tags = True
	download_url.short_description = 'Download'

	def run_checker_url(self,solution):
		return '<a href="%s">Run Checkers</a>' % (reverse('solution_run_checker', args=[solution.id]))
	run_checker_url.allow_tags = True
	run_checker_url.short_description = 'Run Checker (incl. those run at submission)'

	def show_author(self,instance):
		return format_html('<a href="{0}">{1}</a>',
                    reverse('admin:accounts_user_change', args=(instance.author.pk,)),
                    instance.author)
	show_author.allow_tags = True
	show_author.short_description = 'Solution author'

        def useful_links(self, instance):
                return format_html ('<a href="{0}">Attestations of this solution</a> • <a href="{1}">User Site view of this solution</a>',
                    reverse('admin:attestation_attestation_changelist') + ("?solution__exact=%d" % instance.pk),
                    reverse('solution_detail', args=[instance.pk])
                    )
        useful_links.allow_tags = True



	def latest_of_only_failed(self,solution):
		successfull_solution_from_user_for_task_available = solution.final or  [ s for s in Solution.objects.all().filter(author=solution.author,task=solution.task) if s.final]
		is_latest_failed_attempt = (not solution.final) and (Solution.objects.all().filter(task=solution.task,author=solution.author).aggregate(Max('number'))['number__max'] == solution.number)
		return (not successfull_solution_from_user_for_task_available) and is_latest_failed_attempt
	latest_of_only_failed.boolean = True

admin.site.register(Solution, SolutionAdmin)
	








