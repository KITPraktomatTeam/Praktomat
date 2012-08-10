from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import login
from django.conf import settings

from accounts.models import User
from django.contrib.auth.models import Group
from accounts.forms import MyRegistrationForm

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
	httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
	return HttpResponseForbidden(loader.render_to_string(*args, **kwargs),
									 **httpresponse_kwargs)

def shib_hello(request):
	return render_to_response('registration/shib_hello.html', {'title':"Login via shibboleth", 'provider': settings.SHIB_PROVIDER}, RequestContext(request))

def shib_login(request):
	attr, error = parse_attributes(request.META)

	was_redirected = False
	if "next" in request.REQUEST:
		was_redirected = True
	redirect_url = request.REQUEST.get('next', settings.LOGIN_REDIRECT_URL)
	context = {'shib_attrs': attr,
			   'was_redirected': was_redirected}
	if error:
		return render_forbidden('shibboleth/attribute_error.html',
								  context,
								  context_instance=RequestContext(request))
	try:
		username = attr[settings.SHIB_USERNAME]
		# TODO this should log a misconfiguration.
	except:
		return render_forbidden('shibboleth/attribute_error.html',
								  context,
								  context_instance=RequestContext(request))

	if not attr[settings.SHIB_USERNAME] or attr[settings.SHIB_USERNAME] == '':
		return render_forbidden('shibboleth/attribute_error.html',
								  context,
								  context_instance=RequestContext(request))

	try:
		user = User.objects.get(username=attr[settings.SHIB_USERNAME])
	except User.DoesNotExist:
		user = User.objects.create_user(attr[settings.SHIB_USERNAME],'')
		user_group = Group.objects.get(name='User')
		user.groups.add(user_group)

	# This needs to be made more general smarter
	user.first_name = attr['first_name']
	user.last_name = attr['last_name']
	user.email = attr['email']
	user.mat_number = int("12345")
	user.save()

	user.backend = 'django.contrib.auth.backends.ModelBackend'
	login(request, user)

	if not redirect_url or '//' in redirect_url or ' ' in redirect_url:
		redirect_url = settings.LOGIN_REDIRECT_URL

	return HttpResponseRedirect(redirect_url)



