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
    title = 'latest of only failed'
    parameter_name = 'latest_of_only_failed'

    def lookups(self, request, model_admin):
        return (
          ('Yes','Yes'),
          ('No','No'),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'Yes':
            return queryset.filter(_latest_of_only_failed_computed_for_sorting=True)
        elif value == 'No':
            return queryset.filter(_latest_of_only_failed_computed_for_sorting=False)
        return queryset


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







class SolutionAdmin(admin.ModelAdmin):
    model = Solution
    list_display = ["edit", "view_url", "download_url", "run_checker_url", "task", "show_author", "number", "creation_date", "final", "accepted", "tests_failed" ,"latest_of_only_failed", "plagiarism"]
    list_filter = ["task", "author", "author__groups", "creation_date" , IsLatestOfOnlyFailedFilter ,"final", "accepted", "warnings", "plagiarism"]
    fieldsets = ((None, {
                    'fields': ( "task", "show_author", "creation_date", ("final", "accepted", "warnings"), "plagiarism", 'useful_links')
                }),)
    readonly_fields=["task", "show_author", "creation_date", "accepted", "final", "tests_failed", 'useful_links']
    inlines =  [CheckerResultInline, SolutionFileInline]
    actions = ['run_checkers', 'run_checkers_all', 'mark_plagiarism', 'mark_no_plagiarism']

    #for sorting computed values "tests_failed" and "latest of only failed" which are not stored in database,
    #wie have to implement the behavior of get_queryset to simulate a return of SQL's ORDER BY

    def get_queryset(self, request):
        queryset = super(SolutionAdmin,self).get_queryset(request)
        from django.db.models import BooleanField
        from django.db.models import Exists, OuterRef , F , Value
        from django.db.models.expressions import RawSQL

        #example snipplet 1
        # events = Event.objects.all().annotate(paid_participants=models.Sum(
        #   models.Case(
        #             models.When(participant__is_paid=True, then=1),
        #             default=0,
        #             output_field=models.IntegerField()
        # )))

        #example snipplet 2
        # Item.objects.filter(serial__in=license_ids
        # ).update(renewable=Case(
        #     When(renewable=True, then=Value(False)),
        #     default=Value(True))
        #     )
        # )

        #example snipplet 3
        #Join chains can be as deep as you require. For example, to extract the age of the youngest author of any book available for sale, you could issue the query:
        #>>> Store.objects.aggregate(youngest_age=Min('books__authors__age'))

        #example snipplet 4
        # _computed_value= ExpressionWrapper(
        # F('entiyAttributeOne') < F('otherEntity__'), output_field=BooleanField()))

        queryset = queryset.annotate(
             # Outside the query annotation, we would get the the correct value for each mysolution with:
             # CheckerResult.objects.filter(solution=mysolution,passed=False).exists();
             #
             # In pure SQL we could use a correlated Subquery with EXISTS in outer SELECT-statement:
             # SELECT EXISTS
             #    (
             #       SELECT c.id AS checkerID
             #       FROM checker_checkerresult c
             #       WHERE ( (NOT c.passed) AND (c.solution_id = s.id))
             #    ) AS "has failed Checkers"
             # FROM solutions_solution s

            _tests_failed_computed_for_sorting=  Exists( CheckerResult.objects.only('id').filter( solution_id=OuterRef('id'),passed=False)) ,


            # In pure SQL we could use a correlated Subquery with EXISTS in outer SELECT-statement:
            #
            # I did not find any possibility to use the Django ORM-Manager for writing it, therefor I am now using RawSQL

            _latest_of_only_failed_computed_for_sorting=RawSQL(
              '''SELECT EXISTS(
                   SELECT s.id, s.final, s.accepted, s.author_id
                   FROM solutions_solution s
                   WHERE ((Not s.final) and (Not s.accepted))
                           AND (s.author_id, s.task_id) NOT IN ( SELECT i.author_id, i.task_id
                                                        FROM solutions_solution i
                                                        WHERE i.final )
                   GROUP BY s.author_id, s.task_id
                   HAVING MAX(s.number) == s.number
                   AND s.id == o.id
                 ) as latest_of_only_failed
                 FROM solutions_solution o
                 WHERE o.id = solutions_solution.id
                 ''', []),  #OuterRef('id')  --- because we cannot use OuterRef as parameter , I coded solutions_solution.id in a hard way ...
           )
        return queryset





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
        #return CheckerResult.objects.filter(solution=solution,passed=False).exists();
        #since we had annotated the queryset already, for sorting this computed column, just reuse that annotated values for visualisation
        return solution._tests_failed_computed_for_sorting
    tests_failed.boolean = True
    tests_failed.admin_order_field = '_tests_failed_computed_for_sorting'


    def latest_of_only_failed(self, solution):
        # ToDo ... perhaps to slow for many solutions ... rethink about it using subqueries:
        # https://hansonkd.medium.com/the-dramatic-benefits-of-django-subqueries-and-annotations-4195e0dafb16
        # https://medium.com/kolonial-no-product-tech/pushing-the-orm-to-its-limits-d26d87a66d28
        #successfull_solution_from_user_for_task_available = solution.final or  [ s for s in Solution.objects.all().filter(author=solution.author, task=solution.task) if s.final]
        #is_latest_failed_attempt = (not solution.final) and (Solution.objects.all().filter(task=solution.task, author=solution.author).aggregate(Max('number'))['number__max'] == solution.number)
        #return (not successfull_solution_from_user_for_task_available) and is_latest_failed_attempt

        #since we had annotated the queryset already, for sorting this computed column, just reuse that annotated values for visualisation
        #on Admin Solution change listview the green circle is "Yes"
        # => here "Yes" means "latest of only failed solution" and that is not a "positive" information
        # => therfor it would be better to change the symbolic - like mentioned in https://github.com/KITPraktomatTeam/Praktomat/issues/315
        return solution._latest_of_only_failed_computed_for_sorting
    latest_of_only_failed.boolean = True
    latest_of_only_failed.admin_order_field = '_latest_of_only_failed_computed_for_sorting'


admin.site.register(Solution, SolutionAdmin)
