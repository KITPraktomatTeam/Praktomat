import datetime

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render_to_response, resolve_url
from django.contrib.auth import login
from django.conf import settings
from django.db import transaction

from accounts.models import User
from django.contrib.auth.models import Group
from accounts.forms import MyRegistrationForm
from accounts.decorators import *

from configuration import get_settings

def parse_attributes(META):
	shib_attrs = {}
	error = False
	for header, attr in settings.SHIB_ATTRIBUTE_MAP.items():
		required, name = attr
		values = META.get(header, None)
		value = None
		if values:
			# If multiple attributes releases just care about the 1st one
			try:
				value = values.split(';')[0]
			except:
				value = values
				
		shib_attrs[name] = value
		if not value or value == '':
			if required:
				error = True
	return shib_attrs, error


def render_forbidden(*args, **kwargs):
	return HttpResponseForbidden(loader.render_to_string(*args, **kwargs))

@shibboleth_support_required
def shib_hello(request):
        context = {}
        if 'next' in request.GET:
            context['next'] = request.GET['next']
        context['title'] = "Login via shibboleth"
        context['provider'] = settings.SHIB_PROVIDER
	return render_to_response('registration/shib_hello.html', context, RequestContext(request))

@shibboleth_support_required
@transaction.atomic
def shib_login(request):
	attr, error = parse_attributes(request.META)

	was_redirected = False
	if "next" in request.GET:
		was_redirected = True
	redirect_url = request.GET.get('next', resolve_url(settings.LOGIN_REDIRECT_URL))
	context = {'shib_attrs': attr,
			   'was_redirected': was_redirected}
	if error:
		return render_forbidden('registration/shib_error.html',
								  context,
								  context_instance=RequestContext(request))
	try:
		username = attr[settings.SHIB_USERNAME]
		# TODO this should log a misconfiguration.
	except:
		return render_forbidden('registration/shib_error.html',
								  context,
								  context_instance=RequestContext(request))

	if not attr[settings.SHIB_USERNAME] or attr[settings.SHIB_USERNAME] == '':
		return render_forbidden('registration/shib_error.html',
								  context,
								  context_instance=RequestContext(request))

	try:
		user = User.objects.get(username=attr[settings.SHIB_USERNAME])
	except User.DoesNotExist:
            try:
                if attr['matriculationNumber'] is not None:
                    user = User.objects.get(mat_number=attr['matriculationNumber'])
                else:
                    raise User.DoesNotExist
            except:
                if get_settings().new_users_via_sso:
                    user = User.objects.create_user(
			attr[settings.SHIB_USERNAME], '',
			last_login=datetime.datetime.now())
                    user_group = Group.objects.get(name='User')
                    user.groups.add(user_group)
                else:
                    return render_forbidden('registration/shib_not_allowed.html',
								  context,
								  context_instance=RequestContext(request))


	# This needs to be made more general smarter
	user.first_name = attr['first_name']          if attr['first_name'] is not None else user.first_name
	user.last_name = attr['last_name']            if attr['last_name']  is not None else user.last_name
	user.email = attr['email']                    if attr['email']      is not None else user.email
	user.mat_number = attr['matriculationNumber'] if attr['matriculationNumber'] is not None else user.mat_number 
	user.programme  = attr['programme']           if attr['programme']  is not None else user.programme
	user.save()

	user.backend = 'django.contrib.auth.backends.ModelBackend'
	login(request, user)

	if not redirect_url or '//' in redirect_url or ' ' in redirect_url:
		redirect_url = settings.LOGIN_REDIRECT_URL

	return HttpResponseRedirect(redirect_url)

