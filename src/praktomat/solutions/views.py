import zipfile
import tempfile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_detail



from praktomat.tasks.models import Task
from praktomat.solutions.models import Solution, SolutionFile
from praktomat.solutions.forms import SolutionFormSet

@login_required
def solution_list(request, task_id):
	task = get_object_or_404(Task,pk=task_id)
	my_solutions = task.solution_set.filter(author = request.user)
	submission_possible = not task.expired() and not my_solutions.filter(final = True)
	
	if request.method == "POST":	
		solution = Solution(task = task, author=request.user)
		formset = SolutionFormSet(request.POST, request.FILES, instance=solution)
		if formset.is_valid():
			try:
				solution.save()
				formset.save()
				solution.check()
				return HttpResponseRedirect(reverse('solution_detail', args=[solution.id]))
			except:
				solution.delete()	# delete files 
				raise				# dont commit db changes
	else:
		formset = SolutionFormSet()
	return render_to_response("solutions/solution_list.html", {"formset": formset, "task":task, "solutions": my_solutions, "submission_possible":submission_possible},
		context_instance=RequestContext(request))

@login_required
def solution_detail(request,solution_id):
	solution = get_object_or_404(Solution, pk=solution_id)
	submission_possible = not bool(solution.task.solution_set.filter(author=request.user).filter(final = True))
	if solution.author != request.user:
		return render_to_response('error.html', context_instance=RequestContext(request))
	if (request.method == "POST" and solution.accepted):
		solution.final = True
		solution.save()
		return HttpResponseRedirect(reverse('solution_list', args=[solution.task.id]))
	else:	
		return object_detail(request, Solution.objects.all(), solution_id, extra_context={'submission_possible': submission_possible}, template_object_name='solution' )