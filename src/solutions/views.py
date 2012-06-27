import zipfile
import tempfile

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_detail
from django.views.decorators.cache import cache_control
from django.template import Context, loader
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import RequestSite


from datetime import datetime

from tasks.models import Task
from attestation.models import Attestation
from solutions.models import Solution, SolutionFile, get_solutions_zip
from solutions.forms import SolutionFormSet
from accounts.views import access_denied
from accounts.templatetags.in_group import in_group
from accounts.models import User
from configuration import get_settings
from checker.models import CheckerResult
from checker.models import check
from django.db import transaction

@login_required
@transaction.autocommit # allow access to saved solution files before view returns
@cache_control(must_revalidate=True, no_cache=True, no_store=True, max_age=0) #reload the page from the server even if the user used the back button
def solution_list(request, task_id, user_id=None):
	if (user_id and not in_group(request.user,'Trainer')):
		return access_denied(request)

	task = get_object_or_404(Task,pk=task_id)
	author = get_object_or_404(User,pk=user_id) if user_id else request.user
	solutions = task.solution_set.filter(author = author).order_by('-id')
	final_solution = task.final_solution(author)

	if (task.publication_date >= datetime.now()) and (not  in_group(request.user,'Trainer')):
		raise Http404
	
	if request.method == "POST":	
		solution = Solution(task = task, author=author)
		formset = SolutionFormSet(request.POST, request.FILES, instance=solution)
		if formset.is_valid():
			solution.save()
			formset.save()
			run_all_checker = bool(User.objects.filter(id=user_id, tutorial__tutors__pk=request.user.id) or in_group(request.user,'Trainer'))
			solution.check(run_all_checker)
			
			if solution.accepted:  
				# Send submission confirmation email
				t = loader.get_template('solutions/submission_confirmation_email.html')
				c = {
					'protocol': request.is_secure() and "https" or "http",
					'domain': RequestSite(request).domain, 
					'site_name': settings.SITE_NAME,
					'solution': solution,
				}
				if solution.author.email:
					send_mail(_("%s submission confirmation") % settings.SITE_NAME, t.render(Context(c)), None, [solution.author.email])
		
			if solution.accepted or get_settings().accept_all_solutions:
				solution.final = True
				solution.save()
			
			return HttpResponseRedirect(reverse('solution_detail', args=[solution.id]))
	else:
		formset = SolutionFormSet()
	
	attestations = Attestation.objects.filter(solution__task=task, author__tutored_tutorials=request.user.tutorial)
	attestationsPublished = attestations[0].published if attestations else False

	return render_to_response("solutions/solution_list.html", {"formset": formset, "task":task, "solutions": solutions, "final_solution":final_solution, "attestationsPublished":attestationsPublished, "author":author},
		context_instance=RequestContext(request))

@login_required
def solution_detail(request,solution_id,full):
	solution = get_object_or_404(Solution, pk=solution_id)	
	if (not (solution.author == request.user or in_group(request.user,'Trainer') or (solution.author.tutorial and solution.author.tutorial.tutors.filter(id=request.user.id)) )):
		return access_denied(request)

	if (request.method == "POST"):
		solution.copy()
		return HttpResponseRedirect(reverse('solution_list', args=[solution.task.id]))
	else:	
		attestations = Attestation.objects.filter(solution__task=solution.task, author__tutored_tutorials=request.user.tutorial)
		attestationsPublished = attestations[0].published if attestations else False
		return object_detail(request, Solution.objects.all(), solution_id, extra_context={"attestationsPublished":attestationsPublished, "accept_all_solutions":get_settings().accept_all_solutions, "full":full}, template_object_name='solution' )


@login_required
def solution_download(request,solution_id):
	solution = get_object_or_404(Solution, pk=solution_id)	
	if (not (solution.author == request.user or in_group(request.user,'Trainer,Tutor'))):
		return access_denied(request)
	zip_file = get_solutions_zip([solution])
	response = HttpResponse(zip_file.read(), mimetype="application/zip")
	response['Content-Disposition'] = 'attachment; filename=Solution.zip'
	return response

@login_required
def solution_download_for_task(request, task_id):
	if (not in_group(request.user,'Trainer,Tutor')):
		return access_denied(request)

	task = get_object_or_404(Task, pk=task_id)
	solutions = task.solution_set.filter(final=True)
	if not in_group(request.user,'Trainer'):
		solutions = solutions.filter(author__tutorial__id__in=request.user.tutored_tutorials.values_list('id', flat=True))
	zip_file = get_solutions_zip(solutions)
	response = HttpResponse(zip_file.read(), mimetype="application/zip")
	response['Content-Disposition'] = 'attachment; filename=Solutions.zip'
	return response


@login_required
def checker_result_list(request,task_id):
	task = get_object_or_404(Task, pk=task_id)	
	if (not in_group(request.user,'Trainer')):
		return access_denied(request)
	else:

		users_with_checkerresults = [(user,checkerresults,final_solution)                              \
		for user           in User.objects.filter(groups__name='User').order_by('mat_number')          \
		for final_solution in Solution.objects.filter(author=user,final=True,task=task).values() \
		for checkerresults in [sorted(CheckerResult.objects.all().filter(solution=final_solution['id']),key=lambda result : result.checker.order)]]

		number_of_checker = None		
		for checkerresults in users_with_checkerresults:
			if (number_of_checker and (len(checkerresults) != number_of_checker)):
				return acces_denied(request)	#TODO: issue proper error message
			else:
				number_of_checker = len(checkerresults) 

		_, prototype,_ = users_with_checkerresults[0]
		return render_to_response("solutions/checker_result_list.html", {"users_with_checkerresults": users_with_checkerresults,  "prototype":  prototype, "task":task},context_instance=RequestContext(request))

@staff_member_required
def solution_run_checker(request,solution_id):
	solution = Solution.objects.get(pk=solution_id)
	check(solution,True)
	# Since Django suxx (see https://code.djangoproject.com/ticket/8764) and cant mix args with kwargs in reverse(),
	# we suck too, and just mess around with the url
	return HttpResponseRedirect(reverse('solution_detail', args=[solution_id]) + 'full')
