# -*- coding: utf-8 -*-

from django.contrib import admin
from django.shortcuts import render
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.db import transaction
from django.urls import reverse
from tinymce.widgets import TinyMCE
from django.utils.html import format_html

from tasks.models import Task, MediaFile, HtmlInjector
from solutions.models import Solution, SolutionFile
from attestation.admin import RatingAdminInline

import tasks.views

from checker.admin import CheckerInline
from timeit import default_timer as timer

admin.autodiscover()

class MediaInline(admin.StackedInline):
    model = MediaFile
    extra = 0

class HtmlInjectorInline(admin.StackedInline):
    model = HtmlInjector
    extra = 0

class TaskAdmin(admin.ModelAdmin):
    model = Task
    readonly_fields = ('useful_links',)
    fieldsets = (
        (None, {
            'fields': (
                            'title',
                            ('publication_date', 'submission_date'),
                            'description',
                            ('supported_file_types', 'max_file_size'),
                            ('submission_free_uploads', 'submission_waitdelta', 'submission_maxpossible'),
                            'final_grade_rating_scale',
                            'only_trainers_publish',
                            'warning_threshold',
                            'useful_links',
                        )
        }),
    )
    list_display = ('title', 'attestations_url', 'testupload_url', 'publication_date', 'submission_date', 'all_checker_finished')
    list_filter = ['publication_date']
    search_fields = ['title']
    date_hierarchy = 'publication_date'
    save_on_top = True

    inlines = [MediaInline] + [HtmlInjectorInline] + CheckerInline.__subclasses__() + [ RatingAdminInline]
    actions = ['export_tasks', 'run_all_checkers', 'run_all_checkers_on_finals', 'run_all_checkers_on_latest_only_failed', 'delete_attestations', 'unset_all_checker_finished', 'run_all_uploadtime_checkers_on_all']

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

    class Media:
        js = (
                'frameworks/jquery/jquery.js',
                'frameworks/jquery/jquery-ui.js',
                'frameworks/jquery/jquery.tinysort.js',
                'script/checker-sort.js',
        )


    def export_tasks(self, request, queryset):
        """ Export Task action """
        from django.http import HttpResponse
        response = HttpResponse(Task.export_Tasks(queryset).read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename=TaskExport.zip'
        return response


    def run_all_checkers_on_finals(self, request, queryset):
        """ Rerun all checker on final solutions including "not always" action """
        start = timer()
        count = 0
        for task in queryset:
            count += task.check_all_final_solutions()
        end = timer()
        self.message_user(request, "%d final solutions were successfully checked (%d seconds elapsed)." % (count, end-start))
    run_all_checkers_on_finals.short_description = "check only finals (Admin)"

    def run_all_checkers_on_latest_only_failed(self,request, queryset):
        """ Rerun all checker on latest of only failed solutions including "not always" action """
        start = timer()
        count = 0
        for task in queryset:
            count += task.check_all_latest_only_failed_solutions()
        end = timer()
        self.message_user(request, "%d users with only failed solutions were checked (%d seconds elapsed)." % (count, end-start))
    run_all_checkers_on_latest_only_failed.short_description = "recheck only latest failed (Admin)"


    def run_all_checkers(self, request, queryset):
        """ Rerun all checker including "not always" action for students with final or latest of only failed solutions """
        self.run_all_checkers_on_finals(request, queryset)
        self.run_all_checkers_on_latest_only_failed(request, queryset)
    run_all_checkers.short_description = "run all checkers (Trainer)"

    def delete_attestations(self, request, queryset):
        """ delete given attestations for task solutions """
        from attestation.models import Attestation
        start = timer()
        count = 0
        tcount = 0
        for task in queryset:
                        solution_set = Solution.objects.filter(task=task.id)
                        for sol in solution_set :
                                for a in Attestation.objects.filter(solution=sol):
                                        a.delete()
                                        count += 1
                        tcount += 1
        end = timer()
        self.message_user(request, "Deleted %d Attestations over %d Tasks: LoopTimer: %d " %(count, tcount, end-start),"warning")
    delete_attestations.short_description = "delete attestations (Admin)"

    def run_all_uploadtime_checkers_on_all(self, request, queryset):
        """ Rerun on all solutions all checkers which are running at uploadtime """
        from checker.basemodels import check_multiple, check_solution
        from accounts.models import User
        from django.template import Context, loader
        from django.contrib.sites.requests import RequestSite
        from django.conf import settings
        from django.core.mail import send_mail
        from django.utils.translation import ugettext_lazy as _
        myRequestUser = User.objects.filter(id=request.user.id)
        allstart = timer()
        task_set = queryset
        for task in task_set:
            start = timer()
             #solutions = Solution.objects.filter(task=task.id).order_by('author', 'number')
            solution_set = task.solution_set.order_by('author','number')

            old_final_solution_set =  solution_set.filter(final=True)
            users_with_old_final_solution = list(set(old_final_solution_set.values('author').values_list('author',flat = True)))

            for solution in old_final_solution_set:
                solution.final = False
                solution.accepted = False
                solution.save()

            #TODO: some how inform user how long time they must wait until this method will be finish.
            #print("rerun checkers ... wait much time ...")
            #this takes many time !!!!
            if  solution_set.count() > 1 :
                check_multiple(solution_set,False)  # just run upload-time_checkers  ... should we ignore Testuploads?
            elif  solution_set.count() == 1 :
                for solution in solution_set :
                    check_solution(solution,False)

            new_accepted_solution_set = Solution.objects.filter(task=task.id , accepted=True , testupload=False ).order_by('author', 'number')
            users_with_accepted_solutions = list(set(
                                                         new_accepted_solution_set.values('author').values_list('author', flat=True)
                                                        ))


            for userid in users_with_accepted_solutions :
                new_final_solution = new_accepted_solution_set.filter(author = userid).latest('number')
                new_final_solution.final = True
                new_final_solution.save()


            new_final_solution_set =  new_accepted_solution_set.filter(final=True)
            users_with_final_solution =  list(set(new_final_solution_set.values('author').values_list('author',flat = True)))

            users_missing_in_new_final_solution = list(set(users_with_old_final_solution) - set(users_with_final_solution))
            missing_users_in_new_final_solution_set = task.solution_set.filter(author__in=users_missing_in_new_final_solution).order_by('author','number')

            for userid in users_missing_in_new_final_solution :
                user = User.objects.filter(id=userid)
                latestfailed_user_solution = missing_users_in_new_final_solution_set.filter(author=userid).latest('number')
                # Send final solution lost email to current RequestUser tutor/trainer/superuser
                t = loader.get_template('solutions/submission_final_lost_email.html')
                c = {
                                        'protocol': request.is_secure() and "https" or "http",
                                        'domain': RequestSite(request).domain,
                                        'site_name': settings.SITE_NAME,
                                        'solution': latestfailed_user_solution,
                                        'request_user': myRequestUser,
                }
                if request.user.email and latestfailed_user_solution.author.email:
                    send_mail(_("[%s] lost final submission confirmation") % settings.SITE_NAME, t.render(c), None, [request.user.email, latestfailed_user_solution.author.email])
                elif request.user.email and not latestfailed_user_solution.author.email:
                    send_mail(_("[%s] lost final submission confirmation") % settings.SITE_NAME, t.render(c), None, [request.user.email])
                elif not request.user.email and latestfailed_user_solution.author.email:
                    send_mail(_("%s lost final submission confirmation") % settings.SITE_NAME, t.render(c), None, [latestfailed_user_solution.author.email])
            end = timer()
            self.message_user(request, "Task %s : Checked %d authors lost their finals: LoopTimer: %d seconds elapsed "%(task.title, len(users_missing_in_new_final_solution),(end-start)),"warning")
        allend = timer()
        self.message_user(request, "%d Tasks rechecked : LoopTimer: %d seconds elapsed" % (task_set.count(),allend-allstart))
    run_all_uploadtime_checkers_on_all.short_description = "recheck all submissions with uploadtime checker (Admin)"


    def unset_all_checker_finished(self, request, queryset):
        """ Unset task attribute: all_checker_finished """
        start = timer()
        count = 0
        for task in queryset:
            task.all_checker_finished = False
            task.save()
            count += 1
        end = timer()
        self.message_user(request, "State of attribute \"all_checker_finished\" at %d Tasks resetted to \"FALSE\": LoopTimer: %d " % (count, end-start),"warning")
    unset_all_checker_finished.short_description = "unset all checker finished (Admin)"



    def get_urls(self):
        """ Add URL to task import """
        urls = super(TaskAdmin, self).get_urls()
        from django.conf.urls import url
        my_urls = [url(r'^import/$', tasks.views.import_tasks, name='task_import')]
        return my_urls + urls

    def attestations_url(self, task):
        return format_html ('<a href="{0}">Attestations (User site)</a>',
                            reverse('attestation_list', kwargs={'task_id': task.id}))
    attestations_url.short_description = 'Attestations'

    def testupload_url(self, task):
        return format_html ('<a href="{0}">Test Submission</a>',
                            reverse('upload_test_solution', kwargs={'task_id': task.id}))
    testupload_url.short_description = 'Test Submission'

    def useful_links(self, instance):
        if instance.id:
            return format_html (
                '<a href="{0}">Attestations (including for-user-submission)</a> • ' +
                '<a href="{1}">Test upload</a>',
                reverse('attestation_list', kwargs={'task_id': instance.id}),
                reverse('upload_test_solution', kwargs={'task_id': instance.id})
                )
        else:
            return ""


admin.site.register(Task, TaskAdmin)
