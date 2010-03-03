from datetime import datetime
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
	submission_possible = task.submission_date > datetime.now()	and not my_solutions.filter(final = True)
	
	if request.method == "POST":
			
		solution = Solution(task = task, author=request.user)
		formset = SolutionFormSet(request.POST, request.FILES, instance=solution)
		if formset.is_valid():
			try:
				request.session['checker_progress'] = 0
				request.session.save()
				solution.save()
				instances = formset.save(commit=False)
				from django.core.files import File
				for solution_file in instances:
					if solution_file.file.name[-3:].upper() == 'ZIP':
						zip = zipfile.ZipFile(solution_file.file, 'r')
						for zip_file_name in zip.namelist():
							#assert False
							if not SolutionFile.ignorred_file_names_re.match(zip_file_name):
								new_solution_file = SolutionFile(solution=solution)
								temp_file = tempfile.NamedTemporaryFile()						# autodeleted
								temp_file.write(zip.open(zip_file_name).read()) 
								new_solution_file.file.save(zip_file_name, File(temp_file), save=True)		# need to check for filenames begining with / or ..?
					else:
						solution_file.save()
				solution.check(request.session)
				# the form's submit targets an iframe, this allaows webkit based browsers (and probably others) to make ajax calls while posting
				# so we are returning an javascript which will redirect the parent window of the iframe 
				return render_to_response("solutions/js_redirect.html", {"redirect_url": reverse('solution_detail', args=[solution.id])}, context_instance=RequestContext(request))
				#return HttpResponseRedirect(reverse('solution_detail', args=[solution.id]))
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