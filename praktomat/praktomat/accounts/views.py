from praktomat.accounts.forms import MyRegistrationForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from praktomat.accounts.models import UserProfile

def register(request):
	if request.method == 'POST':
	        form = MyRegistrationForm(request.POST)
	        if form.is_valid():
	            form.save()
	            return HttpResponseRedirect(reverse('registration_complete'))
	else:
	        form = MyRegistrationForm()
	return render_to_response('registration/registration_form.html',{'form':form}, context_instance=RequestContext(request))

def activate(request, activation_key):
	account = UserProfile.activate_user(activation_key)
	#assert False
	return render_to_response('registration/registration_activated.html',
							{ 'account': account, 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS }, 
							context_instance=RequestContext(request))
