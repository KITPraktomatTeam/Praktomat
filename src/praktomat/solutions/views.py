import zipfile
import tempfile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_detail
from django.views.decorators.cache import cache_control
from django.template import Context, loader
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import RequestSite

from praktomat.tasks.models import Task
from praktomat.attestation.models import Attestation
from praktomat.solutions.models import Solution, SolutionFile
from praktomat.solutions.forms import SolutionFormSet
from praktomat.accounts.views import access_denied

from django.db import transaction

@login_required
@transaction.autocommit # allow access to saved solution files before view returns
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
			
			# Send submission confirmation email
			t = loader.get_template('solutions/submission_confirmation_email.html')
			c = {
				'protocol': request.is_secure() and "https" or "http",
				'domain': RequestSite(request).domain, 
				'site_name': settings.SITE_NAME,
				'solution': solution,
			}
			send_mail(_("%s submission conformation") % settings.SITE_NAME, t.render(Context(c)), None, [solution.author.email])
			
			return HttpResponseRedirect(reverse('solution_detail', args=[solution.id]))
	else:
		formset = SolutionFormSet()
	
	attestations = Attestation.objects.filter(solution__task=task, author__tutored_tutorials=request.user.tutorial)
	attestationsPublished = attestations[0].published if attestations else False

	return render_to_response("solutions/solution_list.html", {"formset": formset, "task":task, "solutions": my_solutions, "attestationsPublished":attestationsPublished},
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
		attestations = Attestation.objects.filter(solution__task=solution.task, author__tutored_tutorials=request.user.tutorial)
		attestationsPublished = attestations[0].published if attestations else False
		return object_detail(request, Solution.objects.all(), solution_id, extra_context={"attestationsPublished":attestationsPublished}, template_object_name='solution' )
