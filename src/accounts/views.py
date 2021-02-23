#from accounts.forms import MyRegistrationForm
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.template import Template, loader
from django.conf import settings
from accounts.forms import MyRegistrationForm, UserChangeForm, ImportForm, ImportTutorialAssignmentForm, ImportMatriculationListForm, ImportUserTextsForm, AcceptDisclaimerForm
from accounts.models import User, Tutorial
from accounts.decorators import local_user_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.requests import RequestSite
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.http import int_to_base36
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from configuration import get_settings

import csv
import io

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
    return render(request, 'registration/registration_form.html', extra_context)

def activate(request, activation_key):
    account = User.activate_user(activation_key)
    return render(request, 'registration/registration_activated.html', { 'account': account, 'expiration_days': get_settings().acount_activation_days })

@staff_member_required
def activation_allow(request, user_id):
    user = get_object_or_404(User, pk=user_id)
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
    send_mail(_("Account activation on %s") % settings.SITE_NAME, t.render(c), None, [user.email])
    return render(request, 'registration/registration_activation_allowed.html', { 'new_user': user, })

@local_user_required
def change(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('task_list'))
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'registration/registration_change.html', {'form':form, 'user':request.user})

@login_required
def view(request):
    return render(request, 'registration/registration_view.html', {'user':request.user})

def access_denied(request):
    request_path = request.META.get('HTTP_HOST', '') + request.get_full_path()
    res = render(request,
            'access_denied.html',
            {'request_path': request_path})
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
                            send_mail(_("Account activation on %s") % settings.SITE_NAME, t.render(c), None, [user.email])
                return HttpResponseRedirect(reverse('admin:accounts_user_changelist'))
            except:
                raise
                from django.forms.utils import ErrorList
                msg = "An Error occured. The import file was probably malformed."
                form._errors["file"] = ErrorList([msg])
    else:
        form = ImportForm()
    return render(request, 'admin/accounts/user/import.html', {'form': form, 'title':"Import User" })

@staff_member_required
def import_tutorial_assignment(request):
    """ View in the admin """
    if request.method == 'POST':
        form = ImportTutorialAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.files['csv_file']
            file.seek(0)
            try:
                reader = csv.reader(io.StringIO(file.read().decode('utf-8')), delimiter=str(form.cleaned_data['delimiter']), quotechar=str(form.cleaned_data['quotechar']))
            except UnicodeDecodeError as e:
                messages.error(request, "Import failed: %s" % str(e))
                return render(request, 'admin/accounts/user/import_tutorial_assignment.html', {'form': form, 'title':"Import tutorial assignment"  })
            succeeded = not_present = failed = 0
            for row in reader:
                try:
                    matching_users = User.objects.filter(mat_number = row[form.cleaned_data['mat_coloum']])
                    if not matching_users.exists():
                        not_present += 1
                        continue
                    user = matching_users.get()
                    tutorial = Tutorial.objects.get(name = row[form.cleaned_data['name_coloum']])
                    user.tutorial = tutorial
                    user.save()
                    succeeded += 1
                except:
                    failed += 1
            #assert False
            messages.warning(request, "%i assignments were imported successfully, %i users not found, %i failed." % (succeeded, not_present, failed))
            return HttpResponseRedirect(reverse('admin:accounts_user_changelist'))
    else:
        form = ImportTutorialAssignmentForm()
    return render(request, 'admin/accounts/user/import_tutorial_assignment.html', {'form': form, 'title':"Import tutorial assignment"  })

@staff_member_required
def import_user_texts(request):
    """ View in the admin """
    if request.method == 'POST':
        form = ImportUserTextsForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.files['csv_file']
            file.seek(0)
            try:
                reader = csv.reader(io.StringIO(file.read().decode('utf-8')), delimiter=str(form.cleaned_data['delimiter']), quotechar=str(form.cleaned_data['quotechar']))
            except UnicodeDecodeError as e:
                messages.error(request, "Import failed: %s" % str(e))
                return render(request, 'admin/accounts/user/import_user_texts.html', {'form': form, 'title':"Import user texts"  })
            succeeded = not_present = failed = 0
            for row in reader:
                try:
                    matching_users = User.objects.filter(mat_number = row[0])
                    if not matching_users.exists():
                        not_present += 1
                        continue
                    user = matching_users.get()
                    user.user_text = row[1]
                    user.clean_fields()
                    user.save()
                    succeeded += 1
                except:
                    failed += 1
            #assert False
            messages.warning(request, "%i user texts were imported successfully, %i users not found, %i failed." % (succeeded, not_present, failed))
            return HttpResponseRedirect(reverse('admin:accounts_user_changelist'))
    else:
        form = ImportUserTextsForm()
    return render(request, 'admin/accounts/user/import_user_texts.html', {'form': form, 'title':"Import user texts"  })

@staff_member_required
def import_matriculation_list(request, group_id):
    """ Set the group membership of all users according to an uploaded list of matriculation numbers. """
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = ImportMatriculationListForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.files['mat_number_file']
            file.seek(0)
            reader = csv.reader(io.StringIO(file.read().decode('utf-8')))
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
            return HttpResponseRedirect(reverse('admin:auth_group_change', args=[group_id]))
    else:
        form = ImportMatriculationListForm()
    return render(request, 'admin/auth/group/import_matriculation_list.html', {'form': form, 'title':"Import matriculation number list"})

def deactivated(request):
    return render(request, 'registration/registration_deactivated.html')

def accept_disclaimer(request):
    if request.method == 'POST':
        form = AcceptDisclaimerForm(request.POST)
        if form.is_valid():
            # the following should be enforced by the form but check again, just to be sure
            if form.cleaned_data['accept_disclaimer']:
                request.user.accepted_disclaimer = True
                request.user.save()
                return HttpResponseRedirect(reverse('index'))
    else:
        form = AcceptDisclaimerForm()
    return render(request, 'registration/accept_disclaimer.html', {'form' : form})
