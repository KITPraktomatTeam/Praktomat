#from praktomat.accounts.forms import MyRegistrationForm
from datetime import date
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from praktomat.accounts.forms import MyRegistrationForm, UserChangeForm
from praktomat.accounts.models import User
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site, RequestSite

def register(request):
	extra_context = {}
	if settings.DENY_REGISTRATION_FROM < date.today():
		extra_context['deny_registration_from'] = settings.DENY_REGISTRATION_FROM
		extra_context['admins'] = User.objects.filter(is_superuser=True)
		extra_context['trainers'] = Group.objects.get(name="Trainer").user_set.all()
	else:
		if request.method == 'POST':
			form = MyRegistrationForm(request.POST, domain=RequestSite(request).domain, use_https=request.is_secure())
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('registration_complete'))
		else:
			form = MyRegistrationForm()
		extra_context['form'] = form
	return render_to_response('registration/registration_form.html', extra_context, context_instance=RequestContext(request))


def activate(request, activation_key):
	account = User.activate_user(activation_key)
	return render_to_response('registration/registration_activated.html', { 'account': account, 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS }, context_instance=RequestContext(request))


def change(request):
	if request.method == 'POST':
		form = UserChangeForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('task_list'))
	else:
		form = UserChangeForm(instance=request.user)
	return render_to_response('registration/registration_change.html', {'form':form}, context_instance=RequestContext(request))

def access_denied(request):
	request_path = request.META['HTTP_HOST'] + request.get_full_path()
	return render_to_response('access_denied.html', {'request_path': request_path}, context_instance=RequestContext(request))
