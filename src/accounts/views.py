#from accounts.forms import MyRegistrationForm
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, Template, Context, loader
from django.conf import settings
from accounts.forms import MyRegistrationForm, UserChangeForm, ImportForm, ImportLDAPForm, ImportTutorialAssignmentForm, ImportMatriculationListForm
from accounts.models import User, Tutorial
from accounts.decorators import local_user_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.requests import RequestSite
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core import urlresolvers
from django.utils.http import int_to_base36
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from configuration import get_settings
from accounts.ldap_auth import fetch_ldapuser_dict, create_localuser_from_ldapuser

import csv

def register(request):
	extra_context = {}
	if (not settings.REGISTRATION_POSSIBLE) or get_settings().deny_registration_from < datetime.now():
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
	return render_to_response('registration/registration_activated.html', { 'account': account, 'expiration_days': get_settings().acount_activation_days }, context_instance=RequestContext(request))

@staff_member_required
def activation_allow(request,user_id):
	user = get_object_or_404(User,pk=user_id)
	# Send activation email
	t = loader.get_template('registration/registration_email.html')
	c = {
		'email': user.email,
		'domain': RequestSite(request).domain,
		'site_name': settings.SITE_NAME,
		'uid': int_to_base36(user.id),
		'user': user,
		'protocol': request.is_secure() and 'https' or 'http',
		'activation_key': user.activation_key,
		'expiration_days': get_settings().acount_activation_days,
	}
	send_mail(_("Account activation on %s") % settings.SITE_NAME, t.render(Context(c)), None, [user.email])
	return render_to_response('registration/registration_activation_allowed.html', { 'new_user': user, }, context_instance=RequestContext(request))

@local_user_required
def change(request):
	if request.method == 'POST':
		form = UserChangeForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('task_list'))
	else:
		form = UserChangeForm(instance=request.user)
	return render_to_response('registration/registration_change.html', {'form':form, 'user':request.user}, context_instance=RequestContext(request))

@login_required
def view(request):
	return render_to_response('registration/registration_view.html', {'user':request.user}, context_instance=RequestContext(request))

def access_denied(request):
	request_path = request.META.get('HTTP_HOST', '') + request.get_full_path()
	res = render_to_response(
            'access_denied.html',
            {'request_path': request_path},
            context_instance=RequestContext(request))
        res.status_code = 403
        return res

@staff_member_required
def import_user(request):
	""" View in the admin """
	if request.method == 'POST': 
		form = ImportForm(request.POST, request.FILES)
		if form.is_valid(): 
			try:
				imported_user = User.import_user(form.files['file'])
                                messages.success(request, "The import was successfull. %i users imported." % imported_user.count())
				if form.cleaned_data['require_reactivation']:
					for user in [user for user in imported_user if user.is_active]:
						user.is_active = False
						user.set_new_activation_key()
						user.save()
						if form.cleaned_data['send_reactivation_email']:
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
								'expiration_days': get_settings().acount_activation_days,
							}
							send_mail(_("Account activation on %s") % settings.SITE_NAME, t.render(Context(c)), None, [user.email])
				return HttpResponseRedirect(urlresolvers.reverse('admin:accounts_user_changelist'))
			except:
				raise
				from django.forms.utils import ErrorList
				msg = "An Error occured. The import file was propably malformed."
				form._errors["file"] = ErrorList([msg]) 			
	else:
		form = ImportForm()
	return render_to_response('admin/accounts/user/import.html', {'form': form, 'title':"Import User"  }, RequestContext(request))

@staff_member_required
def import_ldap_user(request):
       """ View in the admin """
       if request.method == 'POST': 
               form = ImportLDAPForm(request.POST)
               if form.is_valid():
                       tutorial = form.cleaned_data['tutorial']
                       uids = form.cleaned_data['uids'].split()
                       g = Group.objects.get(name='User')

                       udict = {}
                       unknown_uids = []
                       for uid in uids:
                               udict[uid] = fetch_ldapuser_dict(uid=uid)
                               if udict[uid] is None:
                                       unknown_uids.append(uid)
                       if unknown_uids:
                               messages.add_message(request, messages.ERROR, "ERROR! Import cancelled. Unknown UIDs: %s" % (", ".join(unknown_uids)))
                               return render_to_response('admin/accounts/user/import_ldap.html', {'form':form, 'title':"Import LDAP Users"  }, RequestContext(request))
                       for uid in udict:
                               u = create_localuser_from_ldapuser(username=uid, ldapUser=udict[uid])

                               u.groups.add(g)
                               u.tutorial = tutorial
                               u.save()
               return HttpResponseRedirect(urlresolvers.reverse('admin:accounts_user_changelist'))
       else:
               form = ImportLDAPForm()
       return render_to_response('admin/accounts/user/import_ldap.html', {'form':form, 'title':"Import LDAP Users"  }, RequestContext(request))

@staff_member_required
def import_tutorial_assignment(request):
	""" View in the admin """
	if request.method == 'POST': 
		form = ImportTutorialAssignmentForm(request.POST, request.FILES)
		if form.is_valid(): 
			file = form.files['csv_file']
			reader = csv.reader(file, delimiter=str(form.cleaned_data['delimiter']), quotechar=str(form.cleaned_data['quotechar']))
			succeded = failed = 0
			for row in reader:
				try:
					user = User.objects.get(mat_number = row[form.cleaned_data['mat_coloum']])
					tutorial = Tutorial.objects.get(name = row[form.cleaned_data['name_coloum']])
					user.tutorial = tutorial
					user.save()
					succeded += 1
				except:
					failed += 1
			#assert False
                        messages.warning(request, "%i assignments were imported successfully, %i failed." % (succeded, failed))
			return HttpResponseRedirect(urlresolvers.reverse('admin:accounts_user_changelist'))
	else:
		form = ImportTutorialAssignmentForm()
	return render_to_response('admin/accounts/user/import_tutorial_assignment.html', {'form': form, 'title':"Import tutorial assignment"  }, RequestContext(request))


@staff_member_required
def import_matriculation_list(request, group_id):
    """ Set the group memembership of all users according to an uploaded list of matriculation numbers. """
    group = get_object_or_404(Group,pk=group_id)
    if request.method == 'POST':
        form = ImportMatriculationListForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.files['mat_number_file']
            reader = csv.reader(file)
            mats = set(int(row[0]) for row in reader)

            nr_already = nr_added = nr_removed = nr_new_users = 0

            # first create all users, if required
            if form.cleaned_data['create_users']:
                existing_mats = set(User.objects.values_list('mat_number', flat=True))
                for new in mats - existing_mats:
                    user = User.objects.create_user(new, '')
                    user.groups.add(Group.objects.get(name='User'))
                    user.mat_number = new
                    user.save()
                    nr_new_users += 1

            for u in User.objects.all():
                if u.mat_number in mats:
                    if u.groups.filter(id=group.pk).exists():
                        nr_already += 1
                    else:
                        u.groups.add(group)
                        nr_added += 1
                else:
                    if form.cleaned_data['remove_others']:
                        if u.groups.filter(id=group.pk).exists():
                            u.groups.remove(group)
                            nr_removed += 1
                u.save()
            messages.success(request,
                ("%i users added to group %s, %i removed, %i already in group. "+
                "%i new users created.") % (nr_added, group.name, nr_removed, nr_already, nr_new_users))
            return HttpResponseRedirect(urlresolvers.reverse('admin:auth_group_change', args=[group_id]))
    else:
        form = ImportMatriculationListForm()
    return render_to_response('admin/auth/group/import_matriculation_list.html', {'form': form, 'title':"Import matriuculation number list"}, RequestContext(request))

