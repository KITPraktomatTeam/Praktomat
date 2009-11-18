from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail

from praktomat.tasks.models import Task
from praktomat.solutions.models import Solution, SolutionFile
from praktomat.solutions.forms import SolutionFormSet

@login_required
def statistics(request,task_id):
	task = get_object_or_404(Task,pk=task_id)
	if not (request.user.groups.filter(name='Trainer').values('name') or request.user.is_superuser):
		return render_to_response('error.html', context_instance=RequestContext(request))
	solution_count = task.solution_set.filter(final=True).count()
	from django.contrib.auth.models import Group
	user_count = Group.objects.get(name='User').user_set.count()
	return render_to_response("attestation/statistics.html", {'task':task, 'solution_count': solution_count,'user_count': user_count}, context_instance=RequestContext(request))
	
@login_required
def attestation_list(request, task_id):
	task = Task.objects.get(pk=task_id)
	solutions = Solution.objects.filter(task__id=task_id).filter(final=True).filter(author__userprofile__tutorial__tutors__pk=request.user.id).all()
	return object_list(request, solutions, template_object_name='solution', extra_context={'task':task}, template_name="attestation/attestation_list.html")

	
@login_required
def attestation(request,task_id):
	task = get_object_or_404(Task,pk=task_id)
	if not (request.user.groups.filter(name='Trainer').values('name') or request.user.is_superuser):
		return render_to_response('error.html', context_instance=RequestContext(request))
	solution_count = task.solution_set.filter(final=True).count()
	from django.contrib.auth.models import Group
	user_count = Group.objects.get(name='User').user_set.count()
	return render_to_response("solutions/attestation.html", {'task':task, 'solution_count': solution_count,'user_count': user_count}, context_instance=RequestContext(request))