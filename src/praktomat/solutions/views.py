import zipfile
import tempfile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_detail
from django.views.decorators.cache import cache_control

from praktomat.tasks.models import Task
from praktomat.solutions.models import Solution, SolutionFile
from praktomat.solutions.forms import SolutionFormSet
from praktomat.accounts.views import access_denied

@login_required
@cache_control(must_revalidate=True, no_cache=True, no_store=True, max_age=0) #reload the page from the server even if the user used the back button
def solution_list(request, task_id):
	task = get_object_or_404(Task,pk=task_id)
	my_solutions = task.solution_set.filter(author = request.user).order_by('-id')
	
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
	return render_to_response("solutions/solution_list.html", {"formset": formset, "task":task, "solutions": my_solutions},
		context_instance=RequestContext(request))

@login_required
def solution_detail(request,solution_id):
	solution = get_object_or_404(Solution, pk=solution_id)
	solution.final()
	if solution.author != request.user:
		return access_denied(request)
	if (request.method == "POST"):
		solution.copy()
		return HttpResponseRedirect(reverse('solution_list', args=[solution.task.id]))
	else:	
		return object_detail(request, Solution.objects.all(), solution_id, extra_context={}, template_object_name='solution' )