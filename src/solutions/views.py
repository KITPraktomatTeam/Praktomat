import zipfile
import tempfile

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail, get_connection , mail_admins
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.requests import RequestSite


from datetime import datetime, timedelta

from tasks.models import Task, HtmlInjector
from attestation.models import Attestation
from solutions.models import Solution, SolutionFile, get_solutions_zip, ConfirmationMessage
from solutions.forms import SolutionFormSet
from accounts.views import access_denied
from accounts.models import User
from configuration import get_settings
from checker.basemodels import CheckerResult
from checker.basemodels import check_solution
from django.db import transaction

from utilities.safeexec import execute_arglist

@login_required
@cache_control(must_revalidate=True, no_cache=True, no_store=True, max_age=0) #reload the page from the server even if the user used the back button
def solution_list(request, task_id, user_id=None):
    has_extended_rights = request.user.is_trainer or request.user.is_superuser or (request.user.is_tutor and get_settings().tutors_can_edit_solutions)
    if user_id and not has_extended_rights:
        return access_denied(request)

    task = get_object_or_404(Task, pk=task_id)
    author = get_object_or_404(User, pk=user_id) if user_id else request.user
    solutions = task.solution_set.filter(author = author).order_by('-id')
    final_solution = task.final_solution(author)

    if user_id and request.user.is_tutor and not author in request.user.tutored_users():
        # Tutor not responsible for this user
        return access_denied(request)

    if task.publication_date >= datetime.now() and not request.user.is_trainer:
        raise Http404

    # TODO: Code Refactoring: move code to own function: say linear_waiting
    # linear waiting function
    uploads_left = task.submission_maxpossible - solutions.count()

    minutes_to_wait_for_next_upload = task.submission_waitdelta * ( solutions.count() - task.submission_free_uploads )

    upload_next_possible_time = datetime.now()
    if solutions.count() > 0 :
        upload_next_possible_time = solutions[0].creation_date + timedelta(minutes=minutes_to_wait_for_next_upload)

    dnow = datetime.now()

    # TODO: Code Refactoring: move code to own function: say const_waiting
    #after some time Prof. wish ... don't use a linear waiting function but a constant therefor quick and dirty overwriting "minutes_to_wait_for_next_upload"
    minutes_to_wait_for_next_upload = 1 * task.submission_waitdelta #multiply with one, to be sure getting an integer ...
    if solutions.count() > 0 :
        upload_next_possible_time = solutions[0].creation_date + timedelta(minutes=minutes_to_wait_for_next_upload)


    if request.method == "POST":
        if task.expired() and not has_extended_rights:
            return access_denied(request)
#       fight against multiple open browser window for cheating limits
#       deep defense
        dap = datetime.now() # query datetime after returning from HTTP "post"-method again
        sap = solutions.count() # query solution counter after returning from HTTP "post"-method again
        uap = task.submission_maxpossible - sap
        if not has_extended_rights and (
                                               ((task.submission_free_uploads < 0) or ((task.submission_free_uploads > 0) and (task.submission_free_uploads <= sap )))
                                               and ((task.submission_waitdelta > 0) and (dap < upload_next_possible_time))
                                            or
                                               ((task.submission_maxpossible > 0) and (uap <= 0))
                                            ):
            return access_denied(request)

        solution = Solution(task = task, author=author)
        formset = SolutionFormSet(request.POST, request.FILES, instance=solution)
        if formset.is_valid():
            solution.save()
            try:
                formset.save() # Handle UnicodeEncodeError while saving solution
            except UnicodeError as inst:
                import sys
                extyp, exvalue, ectb = sys.exc_info()
                exnow = datetime.now() # reinserted
                dt_string = exnow.strftime("%d/%m/%Y %H:%M:%S")
                # Send Encoding Error to user via mail
                myRequestUser = User.objects.filter(id=request.user.id)
                myerrmsg = " %s => %s " % (extyp.__name__, exvalue) if exvalue else " %s " %(extyp.__name__,)
                t = loader.get_template('solutions/submission_upload_UnicodeError_email.html')
                c = {
                      'protocol' : request.is_secure() and "https" or "http",
                      'domain' : RequestSite(request).domain,
                      'site_name' : settings.SITE_NAME,
                      'solution' : solution,
                      'request_user': myRequestUser,
                      'errormsg' : myerrmsg,
                      'datetime' : dt_string,
                }
                #ToDo: change to send signed e-mails or unsigned e-mails depending on settings configuration
                send_mail(_("%s submission failed") %settings.SITE_NAME, t.render(c),None, [request.user.email])
                mail_admins(_("%s submission failed") %settings.SITE_NAME, t.render(c))
                raise inst

            #run_all_checker = bool(User.objects.filter(id=user_id, tutorial__tutors__pk=request.user.id) or request.user.is_trainer)
            run_all_checker = bool(User.objects.filter(id=user_id, tutorial__tutors__pk=request.user.id) and task.expired() or request.user.is_trainer and task.expired() )
            solution.check_solution(run_all_checker)

            current_final_solution = Solution.objects.filter(task=task, author=author, final=True).first()
            newer_final_solution_existing = False
            if current_final_solution is not None:
                if current_final_solution.creation_date > solution.creation_date:
                    # The student (re-)submitted another final solution while the checkers were running
                    # This can't be the final solution anymore
                    newer_final_solution_existing = True
            if (solution.accepted or get_settings().accept_all_solutions) and not newer_final_solution_existing:
                solution.final = True
                solution.save()

            if solution.accepted:
                # Send submission confirmation email
                t = loader.get_template('solutions/submission_confirmation_email.html')
                c = {
                    'protocol': request.is_secure() and "https" or "http",
                    'domain': RequestSite(request).domain,
                    'site_name': settings.SITE_NAME,
                    'solution': solution,
                }
                if user_id:
                    # in case someone else uploaded the solution, add this to the email
                    c['uploader'] = request.user

                # we create an smime signed message with openssl, if a private-key and certificate is configured
                if settings.PRIVATE_KEY and settings.CERTIFICATE:
                    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
                        tmp.write("Content-Type: text/plain; charset=utf-8\n")
                        tmp.write("Content-Transfer-Encoding: quoted-printable\n\n")

                        import sys
                        PY2 = sys.version_info[0] == 2
                        PY3 = sys.version_info[0] == 3
                        if PY3:
                            tmp.write(t.render(c))
                            tmp.flush()
                        else:
                            tmp.write(t.render(c).encode('utf-8'))
                            tmp.flush()
                        tmp.seek(0)
                        environ = {}
                        environ['LANG'] = settings.LANG
                        environ['LANGUAGE'] = settings.LANGUAGE
                        [signed_mail, __, __, __, __]  = execute_arglist(["openssl", "smime", "-sign", "-signer", settings.CERTIFICATE, "-inkey", settings.PRIVATE_KEY, "-in", tmp.name], ".", environment_variables=environ, unsafe=True)

                    connection = get_connection()
                    message = ConfirmationMessage(_("%s submission confirmation") % settings.SITE_NAME, signed_mail, None, [solution.author.email], connection=connection)
                    if solution.author.email:
                         message.send() # any PY2-PY3 problem in here ?

                else: #we are sending unsigned email
                    if solution.author.email:
                         send_mail(_("%s submission confirmation") % settings.SITE_NAME, t.render(c), None, [solution.author.email])

            return HttpResponseRedirect(reverse('solution_detail', args=[solution.id]))
    else:
        formset = SolutionFormSet()

    attestations = Attestation.objects.filter(solution__task=task, author__tutored_tutorials=request.user.tutorial)
    attestationsPublished = attestations[0].published if attestations else False


    return render(request, "solutions/solution_list.html",
                {"formset": formset, "task":task, "solutions": solutions, "final_solution":final_solution,  "uploads_left":uploads_left,  "upload_next_possible_time":upload_next_possible_time,  "dnow":dnow, "attestationsPublished":attestationsPublished, "author":author, "invisible_attestor":get_settings().invisible_attestor})


@login_required
def test_upload(request, task_id):
    if not request.user.is_trainer and not request.user.is_tutor and not request.user.is_superuser:
        return access_denied(request)

    task = get_object_or_404(Task, pk=task_id)

    if request.method == "POST":
        solution = Solution(task = task, author=request.user, testupload = True)
        formset = SolutionFormSet(request.POST, request.FILES, instance=solution)
        if formset.is_valid():
            solution.save()
            formset.save()
            solution.check_solution(run_secret = True)

            return HttpResponseRedirect(reverse('solution_detail_full', args=[solution.id]))
    else:
        formset = SolutionFormSet()

    return render(request, "solutions/solution_test_upload.html", {"formset": formset, "task":task})

@login_required
def test_upload_student(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.publication_date >= datetime.now():
        raise Http404

    if request.method == "POST":
        solution = Solution(task = task, author=request.user, testupload = True)
        formset = SolutionFormSet(request.POST, request.FILES, instance=solution)
        if formset.is_valid():
            solution.save()
            formset.save()
            solution.check_solution(run_secret = False)

            return HttpResponseRedirect(reverse('solution_detail', args=[solution.id]))
    else:
        formset = SolutionFormSet()

    return render(request, "solutions/solution_test_upload.html", {"formset": formset, "task":task})

@login_required
def solution_detail(request, solution_id, full):
    solution = get_object_or_404(Solution, pk=solution_id)
    if not (solution.author == request.user or request.user.is_trainer or request.user.is_superuser or (solution.author.tutorial and solution.author.tutorial.tutors.filter(id=request.user.id))):
        return access_denied(request)

    if full and not (request.user.is_trainer or request.user.is_tutor or request.user.is_superuser):
        return access_denied(request)
    
    if request.user.is_user and get_settings().hide_solutions_of_expired_tasks and solution.task.expired():
        return access_denied(request)

    accept_all_solutions = get_settings().accept_all_solutions

    if (request.method == "POST"):
        if solution.final or solution.testupload or solution.task.expired():
            return access_denied(request)
        if not (solution.accepted or accept_all_solutions):
            return access_denied(request)
        solution.copy()
        return HttpResponseRedirect(reverse('solution_list', args=[solution.task.id]))
    else:
        attestations = Attestation.objects.filter(solution__task=solution.task, author__tutored_tutorials=request.user.tutorial)
        attestationsPublished = attestations[0].published if attestations else False
        htmlinjectors = []
        if full:
            htmlinjectors = HtmlInjector.objects.filter(task = solution.task, inject_in_solution_full_view = True)
        else:
            htmlinjectors = HtmlInjector.objects.filter(task = solution.task, inject_in_solution_view      = True)
        htmlinjector_snippets = [ injector.html_file.read().decode("utf-8") for injector in htmlinjectors ]




        return render(request,
                      "solutions/solution_detail.html",
                      {
                        "solution": solution,
                        "attestationsPublished": attestationsPublished,
                        "accept_all_solutions": accept_all_solutions,
                        "htmlinjector_snippets": htmlinjector_snippets,
                        "full":full
                      }
                     )

@login_required
def solution_download(request, solution_id, include_checker_files, include_artifacts):
    solution = get_object_or_404(Solution, pk=solution_id)
    allowed_tutor = request.user.is_tutor and solution.author.tutorial in request.user.tutored_tutorials.all()
    allowed_user = solution.author == request.user and not include_checker_files and not include_artifacts
    hide = request.user.is_user and get_settings().hide_solutions_of_expired_tasks and solution.task.expired()
    if not (request.user.is_trainer or allowed_tutor or allowed_user) or hide:
        return access_denied(request)

    zip_file = get_solutions_zip([solution], include_checker_files, include_artifacts)
    response = HttpResponse(zip_file.read(), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=Solution.zip'
    return response

@login_required
def solution_download_for_task(request, task_id, include_checker_files, include_artifacts):
    if not (request.user.is_tutor or request.user.is_trainer):
        return access_denied(request)

    task = get_object_or_404(Task, pk=task_id)
    solutions = task.solution_set.filter(final=True)
    if not request.user.is_trainer:
        solutions = solutions.filter(author__tutorial__id__in=request.user.tutored_tutorials.values_list('id', flat=True))
    zip_file = get_solutions_zip(solutions, include_checker_files, include_artifacts)
    response = HttpResponse(zip_file.read(), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=Solutions.zip'
    return response

@login_required
def jplag(request, task_id):
    if not (request.user.is_staff):
        return access_denied(request)
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.run_jplag(request.POST['lang'])
        return HttpResponseRedirect(reverse('solution_jplag', args=[task_id]))

    jplag_lang = get_settings().jplag_setting

    return render(request, "solutions/jplag.html", {"task":task, "jplag_lang": jplag_lang})

@login_required
def checker_result_list(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not request.user.is_trainer and not request.user.is_superuser:
        return access_denied(request)
    else:
        users_with_checkerresults = [(user, dict(checkerresults), final_solution)              \
        for user           in User.objects.filter(groups__name='User').order_by('mat_number')          \
        for final_solution in Solution.objects.filter(author=user, final=True, task=task).values() \
        for checkerresults in [[ (result.checker, result) for result in CheckerResult.objects.all().filter(solution=final_solution['id'])]] ]

        checkers_seen = set([])
        for _, results, _  in users_with_checkerresults:
            checkers_seen |= set(results.keys())
        checkers_seen = sorted(checkers_seen, key=lambda checker: checker.order)

        for i, (user, results, final_solution) in enumerate(users_with_checkerresults):
            users_with_checkerresults[i] = (user,
                                            [results[checker] if checker in results else None for (checker) in checkers_seen],
                                            final_solution)

        return render(request, "solutions/checker_result_list.html", {"users_with_checkerresults": users_with_checkerresults,  'checkers_seen':checkers_seen, "task":task})

@staff_member_required
def solution_run_checker(request, solution_id):
    solution = Solution.objects.get(pk=solution_id)
    check_solution(solution, True)
    return HttpResponseRedirect(reverse('solution_detail_full', args=[solution_id]))
