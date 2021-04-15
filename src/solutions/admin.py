# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.contrib import admin
from solutions.models import Solution, SolutionFile
from checker.basemodels import CheckerResult
from checker.basemodels import check_multiple
from django.conf import settings
from django.urls import reverse
from django.db import transaction
from django.db.models import Max
from django.utils.html import format_html
from django.utils.safestring import mark_safe



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


class IsLatestOfOnlyFailedFilter(admin.SimpleListFilter):
    title = 'is_latest_of_only_failed'
    parameter_name = 'latest_of_only_failed'

    def lookups(self, request, model_admin):
        return (
          ('Yes','Yes'),
          ('No','No'),
        )

    def queryset(self, request, queryset):
        value = self.value()

        q=queryset
#        print(type(q))
#        print(q)
        filterlist=[]

        for solution in q:
#           print("=====")
#           print("TaskID:" , solution.task_id)
#           print(solution)
           successfull_solution_from_user_for_task_available = solution.final or  [ s for s in Solution.objects.all().filter(author=solution.author, task=solution.task) if s.final]
#           print("successfull_solution_from_user_for_task_available:", successfull_solution_from_user_for_task_available)
           is_latest_failed_attempt = (not solution.final) and (Solution.objects.all().filter(task=solution.task, author=solution.author).aggregate(Max('number'))['number__max'] == solution.number)
#           print("is_latest_failed_attempt:", is_latest_failed_attempt)
           latestfailed = (not successfull_solution_from_user_for_task_available) and is_latest_failed_attempt
#           print("latestfailed:",latestfailed)
           if True == latestfailed:
#               print("FOUND, put to list" )
               filterlist += [solution.id]
#        print("===============")
#        print(type(filterlist))
#        print(filterlist)
#        print("===============")
        if value == 'Yes':
          return queryset.filter(pk__in=filterlist)
        elif value == 'No':
          return queryset.exclude(pk__in=filterlist)
        return queryset


#    def latest_of_only_failed(self, solution):
#        successfull_solution_from_user_for_task_available = solution.final or  [ s for s in Solution.objects.all().filter(author=solution.author, task=solution.task) if s.final]
#        is_latest_failed_attempt = (not solution.final) and (Solution.objects.all().filter(task=solution.task, author=solution.author).aggregate(Max('number'))['number__max'] == solution.number)
#        return (not successfull_solution_from_user_for_task_available) and is_latest_failed_attempt





class SolutionAdmin(admin.ModelAdmin):
    model = Solution
    list_display = ["edit", "view_url", "download_url", "run_checker_url", "task", "show_author", "number", "creation_date", "final", "accepted", "tests_failed", "latest_of_only_failed", "plagiarism"]
    list_filter = ["task", "author", "author__groups", "creation_date", IsLatestOfOnlyFailedFilter ,"final", "accepted", "warnings", "plagiarism"]
    fieldsets = ((None, {
                    'fields': ( "task", "show_author", "creation_date", ("final", "accepted", "warnings"), "plagiarism", 'useful_links')
                }),)
    readonly_fields=["task", "show_author", "creation_date", "accepted", "final", "tests_failed", 'useful_links']
    inlines =  [CheckerResultInline, SolutionFileInline]
    actions = ['run_checkers', 'run_checkers_all', 'mark_plagiarism', 'mark_no_plagiarism']

    def run_checkers_all(self, request, queryset):
        """ Run Checkers (including those not run at submission) for selected solution """
        check_multiple(queryset, True)
        self.message_user(request, "Checkers (including those not run at submission) for selected solutions were successfully run.")

    run_checkers_all.short_description = "Run Checkers (including those not run at submission) for selected solution "

    def run_checkers(self, request, queryset):
        """ Run Checkers (only those also run at submission) for selected solutions"""
        check_multiple(queryset, False)
        self.message_user(request, "Checkers (only those also run at submission) for selected solutions were successfully run.")

    run_checkers.short_description = "Run Checkers (only those also run at submission) for selected solutions"

    def mod_plagiarism(self, queryset, value):
        count = 0
        for s in queryset:
            if s.plagiarism != value:
                s.plagiarism = value
                s.save()
                count += 1
        return count

    def mark_plagiarism(self, request, queryset):
        count = self.mod_plagiarism(queryset, True)
        self.message_user(request, "%d solutions marked as plagiated" % count)
    mark_plagiarism.short_description = "Mark as plagiated"

    def mark_no_plagiarism(self, request, queryset):
        count = self.mod_plagiarism(queryset, False)
        self.message_user(request, "%d solutions marked as not plagiated" % count)
    mark_no_plagiarism.short_description = "Mark as not plagiated"


    def edit(self, solution):
        return 'Edit'
    edit.short_description = 'Edit (Admin Site)'

    def view_url(self, solution):
        return mark_safe('<a href="%s">View</a>' % (reverse('solution_detail_full', args=[solution.id])))
    view_url.short_description = 'View (User Site)'

    def download_url(self, solution):
        return mark_safe('<a href="%s">Download</a>' % (reverse('solution_download', args=[solution.id])))
    download_url.short_description = 'Download'

    def run_checker_url(self, solution):
        return mark_safe('<a href="%s">Run Checkers</a>' % (reverse('solution_run_checker', args=[solution.id])))
    run_checker_url.short_description = 'Run Checker (incl. those run at submission)'

    def show_author(self, instance):
        return format_html('<a href="{0}">{1}</a>',
                           reverse('admin:accounts_user_change', args=(instance.author.pk,)),
                           instance.author)
    show_author.short_description = 'Solution author'
    show_author.admin_order_field = 'author'

    def useful_links(self, instance):
        if instance.pk:
            return format_html ('<a href="{0}">Attestations of this solution</a> • <a href="{1}">User Site view of this solution</a>',
                reverse('admin:attestation_attestation_changelist') + ("?solution__exact=%d" % instance.pk),
                reverse('solution_detail', args=[instance.pk])
                )
        else:
            return ""

    def tests_failed(self,solution):
        return CheckerResult.objects.filter(solution=solution,passed=False).exists();
    tests_failed.boolean = True

    def latest_of_only_failed(self, solution):
        successfull_solution_from_user_for_task_available = solution.final or  [ s for s in Solution.objects.all().filter(author=solution.author, task=solution.task) if s.final]
        is_latest_failed_attempt = (not solution.final) and (Solution.objects.all().filter(task=solution.task, author=solution.author).aggregate(Max('number'))['number__max'] == solution.number)
        return (not successfull_solution_from_user_for_task_available) and is_latest_failed_attempt
    latest_of_only_failed.boolean = True



admin.site.register(Solution, SolutionAdmin)
