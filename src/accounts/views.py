#from accounts.forms import MyRegistrationForm
from datetime import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, Template, Context
from django.conf import settings
from accounts.forms import MyRegistrationForm, UserChangeForm, ImportForm
from accounts.models import User
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site, RequestSite
from django.contrib.admin.views.decorators import staff_member_required
from django.core import urlresolvers
from django.utils.http import int_to_base36
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from configuration import get_settings

def register(request):
	extra_context = {}
	if get_settings().deny_registration_from < datetime.now():
		extra_context['deny_registration_from'] = get_settings().deny_registration_from
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
	return render_to_response('registration/registration_change.html', {'form':form, 'user':request.user}, context_instance=RequestContext(request))

def access_denied(request):
	request_path = request.META['HTTP_HOST'] + request.get_full_path()
	return render_to_response('access_denied.html', {'request_path': request_path}, context_instance=RequestContext(request))

@staff_member_required
def import_user(request):
	""" View in the admin """
	if request.method == 'POST': 
		form = ImportForm(request.POST, request.FILES)
		if form.is_valid(): 
			try:
				imported_user = User.import_user(form.files['file'])
				request.user.message_set.create(message="The import was successfull. %i users imported." % imported_user.count())
				if form.cleaned_data['require_reactivation']:
					for user in imported_user:
						user.is_active = False
						user.set_new_activation_key()
						user.save()
						# Send activation email
						t = Template(form.cleaned_data['meassagetext'])
						c = {
							'email': user.email,
							'domain': RequestSite(request).domain,
							'site_name': settings.SITE_NAME,
							'uid': int_to_base36(user.id),
							'user': user,
							'protocol': request.is_secure() and 'https' or 'http',
							'activation_key': user.activation_key,
							'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
						}
						send_mail(_("Account activation on %s") % settings.SITE_NAME, t.render(Context(c)), None, [user.email])
				return HttpResponseRedirect(urlresolvers.reverse('admin:accounts_user_changelist'))
			except:
				raise
				from django.forms.util import ErrorList
				msg = "An Error occured. The import file was propably malformed."
				form._errors["file"] = ErrorList([msg]) 			
	else:
		form = ImportForm()
	return render_to_response('admin/accounts/user/import.html', {'form': form, 'title':"Import User"  }, RequestContext(request))