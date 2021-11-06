import datetime

from codecs import decode, encode

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, resolve_url
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

        if not value or value == '':
            if required:
                error = True
        else:
            value = decode(encode(value,"latin-1"), "utf8")
        shib_attrs[name] = value
    return shib_attrs, error


def render_forbidden(request, template_name, context):
    return HttpResponseForbidden(loader.render_to_string(template_name, context, request))

@shibboleth_support_required
def shib_hello(request):
    context = {}
    if 'next' in request.GET:
        context['next'] = request.GET['next']
    context['title'] = "Login via shibboleth"
    context['provider'] = settings.SHIB_PROVIDER
    return render(request, 'registration/shib_hello.html', context)

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
        return render_forbidden(request, 'registration/shib_error.html', context)
    try:
        username = attr[settings.SHIB_USERNAME]
        # TODO this should log a misconfiguration.
    except:
        return render_forbidden(request, 'registration/shib_error.html', context)

    if not attr[settings.SHIB_USERNAME] or attr[settings.SHIB_USERNAME] == '':
        return render_forbidden(request, 'registration/shib_error.html', context)

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
                if get_settings().deny_registration_from < datetime.datetime.now():
                    extra_context = {}
                    extra_context['deny_registration_from'] = get_settings().deny_registration_from
                    extra_context['admins'] = User.objects.filter(is_superuser=True)
                    extra_context['trainers'] = Group.objects.get(name="Trainer").user_set.all()
                    return render(request, 'registration/registration_form.html', extra_context)
                user = User.objects.create_user(
                    attr[settings.SHIB_USERNAME], '',
                    last_login=datetime.datetime.now())
                user_group = Group.objects.get(name='User')
                user.groups.add(user_group)
                if get_settings().account_manual_validation:
                    user.is_active = False
            else:
                return render_forbidden(request, 'registration/shib_not_allowed.html', context)


    # This needs to be made more general smarter
    user.first_name = attr['first_name']          if attr['first_name'] is not None else user.first_name
    user.last_name = attr['last_name']            if attr['last_name']  is not None else user.last_name
    user.email = attr['email']                    if attr['email']      is not None else user.email
    user.mat_number = attr['matriculationNumber'] if attr['matriculationNumber'] is not None else user.mat_number
    user.programme  = attr['programme']           if attr['programme']  is not None else user.programme
    user.save()

    user.backend = settings.AUTH_BACKEND
    login(request, user)

    if not redirect_url or '//' in redirect_url or ' ' in redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    return HttpResponseRedirect(redirect_url)
