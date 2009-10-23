from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail

from praktomat.tasks.models import Task
from praktomat.solutions.models import Solution
from praktomat.solutions.forms import SolutionFormSet

@login_required
def upload_solution(request, task_id):
	task = get_object_or_404(Task,pk=task_id)
	
	if request.method == "POST":
		solution = Solution(task = task, author=request.user)
		formset = SolutionFormSet(request.POST, request.FILES, instance=solution)
		if formset.is_valid():
			solution.save()
			formset.save()
			solution.check()
			return HttpResponseRedirect(reverse('solution_detail', args=[solution.id]))
	else:
		formset = SolutionFormSet()
	return render_to_response("solutions/upload.html", {"formset": formset, "task":task},
		context_instance=RequestContext(request))

@login_required
def solution_detail(request,solution_id):
	if Solution.objects.get(id=solution_id).author != request.user:
		return render_to_response('error.html', context_instance=RequestContext(request))
	return object_detail(request, Solution.objects.all(), solution_id, template_object_name='solution' )
 	