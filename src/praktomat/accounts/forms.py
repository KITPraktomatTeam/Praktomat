import datetime
import random
import hashlib
import re

from django.conf import settings
from django.db import models
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django import forms
from django.contrib.auth.forms import UserCreationForm as UserBaseCreationForm, UserChangeForm as UserBaseChangeForm
from django.core.mail import send_mail
from django.utils.http import int_to_base36

from praktomat.accounts.models import User

class MyRegistrationForm(UserBaseCreationForm):
	
	# overriding modelfields to ensure required fields are provided
	first_name = forms.CharField(max_length = 30,required=True)
	last_name = forms.CharField(max_length = 30,required=True)
	email = forms.EmailField(required=True)
	
	# adding first and last name, email to the form
	class Meta:
		model = User
		fields = ("username","first_name","last_name","email", "mat_number")
	
	def clean_email(self):
		data = self.cleaned_data['email']
		if not re.match(settings.EMAIL_VALIDATION_REGEX, data):
			raise forms.ValidationError("The email you have provided is not valid. It has to be in: " + settings.EMAIL_VALIDATION_REGEX)	
		return data
		
	def save(self):
		user = super(MyRegistrationForm, self).save()
		
		# default group: user
		user.groups = Group.objects.filter(name='User')
		 
		# disable user until activated via email
		user.is_active=False
		
		# The activation key will be a SHA1 hash, generated from a combination of the username and a random salt.
		sha = hashlib.sha1()
		sha.update( str(random.random()) + user.username)
		activation_key = sha.hexdigest()
		user.activation_key=activation_key
		
		user.mat_number=self.cleaned_data.get("mat_number")
		
		user.save()
		
		# Send activation email
		current_site = Site.objects.get_current()
		site_name = current_site.name
		use_https=False
		t = loader.get_template('registration/registration_email.html')
		c = {
			'email': user.email,
			'domain': current_site.domain,
			'site_name': site_name,
			'uid': int_to_base36(user.id),
			'user': user,
			'protocol': use_https and 'https' or 'http',
			'activation_key': activation_key,
			'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
			}
		send_mail(_("Account activation on %s") % site_name, t.render(Context(c)), None, [user.email])
		
		return user
	
class UserCreationForm(UserBaseCreationForm):
	class Meta:
		model = User
		
class UserChangeForm(UserBaseChangeForm):
	class Meta:
		model = User
