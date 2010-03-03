from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail

from praktomat.tasks.models import Task
from praktomat.solutions.models import Solution, SolutionFile
from praktomat.solutions.forms import SolutionFormSet
from praktomat.attestation.models import Attestation, AnnotatedSolutionFile, RatingResult
from praktomat.attestation.forms import AnnotatedFileFormSet, RatingResultFormSet, AttestationForm

@login_required
def statistics(request,task_id):
	task = get_object_or_404(Task, pk=task_id)
	if not (request.user.groups.filter(name='Trainer').values('name') or request.user.is_superuser):
		return render_to_response('error.html', context_instance=RequestContext(request))
	solution_count = task.solution_set.filter(final=True).count()
	from django.contrib.auth.models import Group
	user_count = Group.objects.get(name='User').user_set.count()
	return render_to_response("attestation/statistics.html", {'task':task, 'solution_count': solution_count,'user_count': user_count}, context_instance=RequestContext(request))
	
@login_required
def attestation_list(request, task_id):
	task = Task.objects.get(pk=task_id)
	requestuser = request.user
	solutions = Solution.objects.filter(task__id=task_id).filter(final=True).filter(author__userprofile__tutorial__tutors__pk=request.user.id).all()
	solution_list = map(lambda solution:(solution, not solution.attestations_by(requestuser)), solutions)
	return render_to_response("attestation/attestation_list.html", {'task':task, 'requestuser':requestuser,'solution_list': solution_list}, context_instance=RequestContext(request))
	
@login_required
def new_attestation(request, solution_id):
	#if not (request.user.groups.filter(name='Trainer').values('name') or request.user.is_superuser):
	#	return render_to_response('error.html', context_instance=RequestContext(request))
	solution = get_object_or_404(Solution, pk=solution_id)
	# If there already is an attestation by this user redirect to edit page
	attestations_of_request_user = solution.attestation_set.filter(author=request.user)
	if attestations_of_request_user.count() > 0:
		return HttpResponseRedirect(reverse('edit_attestation', args=[attestations_of_request_user[0].id]))
		
	attest = Attestation(solution = solution, author = request.user)
	attest.save()
	for solutionFile in  solution.solutionfile_set.all():
		annotatedFile = AnnotatedSolutionFile(attestation = attest, solution_file=solutionFile, content=solutionFile.content())
		annotatedFile.save()
	for rating in solution.task.rating_set.all():
		ratingResult = RatingResult(attestation = attest, aspect=rating.aspect)
		ratingResult.save()
	return HttpResponseRedirect(reverse('edit_attestation', args=[attest.id]))
	
		
		
def edit_attestation(request, attestation_id):
	#if not (request.user.groups.filter(name='Trainer').values('name') or request.user.is_superuser):
	#	return render_to_response('error.html', context_instance=RequestContext(request))
	attest = get_object_or_404(Attestation, pk=attestation_id)
	solution = attest.solution
	
	if attest.final or attest.author != request.user:
		# If if this attestation is allready final or not by this user redirect to view_attestation
		return HttpResponseRedirect(reverse('view_attestation', args=[attestation_id]))

	if request.method == "POST":
		attestForm = AttestationForm(request.POST, instance=attest, prefix='attest')
		attestFileFormSet = AnnotatedFileFormSet(request.POST, instance=attest, prefix='attestfiles')
		ratingResultFormSet = RatingResultFormSet(request.POST, instance=attest, prefix='ratingresult')
		if attestForm.is_valid() and attestFileFormSet.is_valid() and ratingResultFormSet.is_valid():
			attestForm.save()
			attestFileFormSet.save()
			ratingResultFormSet.save()
			return HttpResponseRedirect(reverse('view_attestation', args=[attestation_id]))
	else:
		attestForm = AttestationForm(instance=attest, prefix='attest')
		attestFileFormSet = AnnotatedFileFormSet(instance=attest, prefix='attestfiles')
		ratingResultFormSet = RatingResultFormSet(instance=attest, prefix='ratingresult')
	return render_to_response("attestation/attestation_edit.html", {"attestForm": attestForm, "attestFileFormSet": attestFileFormSet, "ratingResultFormSet":ratingResultFormSet, "solution": solution},	context_instance=RequestContext(request))
	
def view_attestation(request, attestation_id):
	
	attest = get_object_or_404(Attestation, pk=attestation_id)

	if request.method == "POST":
		attest.final=True
		attest.save()
		return HttpResponseRedirect(reverse('attestation_list', args=[attest.solution.task.id]))
	else:
		submitable = attest.author == request.user and not attest.final
		return render_to_response("attestation/attestation_view.html", {"attest": attest, 'submitable':submitable},	context_instance=RequestContext(request))











