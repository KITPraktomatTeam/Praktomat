# -*- coding: utf-8 -*-

import tempfile
import zipfile

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django import forms
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
import django.utils.timezone
from django.conf import settings

from tasks.models import Task
from solutions.forms import ModelSolutionFormSet
from solutions.models import Solution, SolutionFile
from accounts.models import User
from accounts.views import access_denied
from attestation.models import Attestation
from attestation.views import user_task_attestation_map
from configuration import get_settings

@login_required
def taskList(request):
    now = django.utils.timezone.now()
    tasks = Task.objects.filter(publication_date__lte = now).order_by('submission_date', 'title')
    expired_Tasks = Task.objects.filter(submission_date__lt = now).order_by('publication_date', 'submission_date', 'title')
    try:
        tutors = request.user.tutorial.tutors.all()
    except:
        tutors = None
    trainers = User.objects.filter(groups__name="Trainer")

    # we only have a single user here, so the rating_list only contains a single row;
    # this row belongs to the given user
    (_, attestations, threshold, calculated_grade) = user_task_attestation_map([request.user], tasks)[0]
    attestations = list(map(lambda a, b: (a,)+b, tasks, attestations))

    def tasksWithSolutions(tasks):
        return [(t, t.final_solution(request.user)) for t in tasks]

    return render(request,
                  'tasks/task_list.html',
                  {
                      'tasks': tasksWithSolutions(tasks),
                      'expired_tasks': tasksWithSolutions(expired_Tasks),
                      'attestations': attestations,
                      'show_final_grade': get_settings().final_grades_published,
                      'tutors': tutors,
                      'trainers': trainers,
                      'threshold': threshold,
                      'calculated_grade': calculated_grade,
                      'user_text': request.user.user_text,
                      'show_contact_link': settings.SHOW_CONTACT_LINK,
                  })

@login_required
def taskDetail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.publication_date >= datetime.now() and not request.user.is_trainer:
        raise Http404

    my_solutions = Task.objects.get(pk=task_id).solution_set.filter(author = request.user)
    return render(request,
                  'tasks/task_detail.html',
                  {
                      'task': task,
                      'solutions': my_solutions,
                  })

class ImportForm(forms.Form):
    file = forms.FileField()
    is_template = forms.BooleanField(initial=True,
                                     required=False,
                                     help_text="Enabled if the imported task is just used as template to create another task. If disabled, the publication date and the rating scale are also imported. This means that students might see the task immediately, and rating scales might be duplicated.")

@staff_member_required
def import_tasks(request):
    """ View in the admin """
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Task.import_Tasks(form.files['file'], request.user, form.cleaned_data['is_template'])
                messages.success(request, "The import was successful.")
                return HttpResponseRedirect(reverse('admin:tasks_task_changelist'))
            except Exception as e:
                from django.forms.utils import ErrorList
                msg = "An Error occurred. The import file was probably malformed: %s" % str(e)
                form._errors["file"] = ErrorList([msg])
    else:
        form = ImportForm()
    return render(request, 'admin/tasks/task/import.html', {'form': form, 'title':"Import Task"  })

@staff_member_required
def download_final_solutions(request, task_id):
    """ download all final solutions of a task from the admin interface """
    zip_file = tempfile.SpooledTemporaryFile()
    zip = zipfile.ZipFile(zip_file, 'w')
    for solution_file in SolutionFile.objects.filter(solution__task=task_id):
        if solution_file.solution.final:
            zip.write(solution_file.file.path, solution_file.file.name)
    zip.close()
    zip_file.seek(0)
    response = HttpResponse(zip_file.read(), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=FinalSolutions.zip'
    return response


@staff_member_required
def model_solution(request, task_id):
    """ View in the admin """
    task = get_object_or_404(Task, pk=task_id)

    if request.method == "POST":
        solution = Solution(task = task, author=request.user)
        formset = ModelSolutionFormSet(request.POST, request.FILES, instance=solution)
        if formset.is_valid():
            try:
                solution.save();
                # no deleting the old solution:
                # delete will cascade on db level deleting checker results and checker
                # as this isn't easily prevented just keep the old solution around until the task is deleted
                formset.save()
                solution.check_solution(request.session)
                task.model_solution = solution;
                task.save()
            except:
                solution.delete()    # delete files
                raise                # don't commit db changes
    else:
        formset = ModelSolutionFormSet()
    context = {"formset": formset, "task": task, 'title': "Model Solution", 'is_popup': True, }
    return render(request, "admin/tasks/task/model_solution.html", context)
