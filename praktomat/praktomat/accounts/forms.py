import datetime
import random
import sha

from django.conf import settings
from django.db import models
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django import forms
from django.contrib.auth.forms import UserCreationForm
from praktomat.accounts.models import UserProfile
from django.core.mail import send_mail
from django.utils.http import int_to_base36

class MyRegistrationForm(UserCreationForm):
	
	# overriding modelfields to ensure required fields are provided
	first_name = forms.CharField(max_length = 30,required=True)
	last_name = forms.CharField(max_length = 30,required=True)
	email = forms.EmailField(required=True)
	
	# add profile fields 
	degree_course = forms.CharField(max_length = 30,required=True)
	mat_number = forms.IntegerField(required=True)
	
	# adding first and last name, email to the form
	class Meta:
		model = User
		fields = ("username","first_name","last_name","email")
	
#	def clean_email(self):
#		data = super(MyRegistrationForm, self).clean_email()
#		# TODO: validate email domain
#		return data
		
	def save(self):
		user = super(MyRegistrationForm, self).save()
		
		# default group: user
		user.groups = Group.objects.filter(name='User')
		 
		# disable user until activated via email
		user.is_active=False
		user.save()
		
		# The activation key will be a SHA1 hash, generated from a combination of the username and a random salt.
		salt = sha.new(str(random.random())).hexdigest()[:5]
		activation_key = sha.new(salt+user.username).hexdigest()
		
		profile = UserProfile(user=user, activation_key=activation_key,
							degree_course=self.cleaned_data.get("degree_course"),
		 					mat_number=self.cleaned_data.get("mat_number")).save()
		
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