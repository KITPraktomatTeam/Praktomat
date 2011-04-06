import datetime
import random
import hashlib
import re

from django.conf import settings
from django.db import models
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import UserCreationForm as UserBaseCreationForm, UserChangeForm as UserBaseChangeForm
from django.core.mail import send_mail
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe

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
		# cleaning the email in the form doesn't validate it in the admin (good for tutors etc.)
		data = self.cleaned_data['email']
		if not re.match(settings.EMAIL_VALIDATION_REGEX, data):
			raise forms.ValidationError("The email you have provided is not valid. It has to be in: " + settings.EMAIL_VALIDATION_REGEX)	
		return data

	def clean_mat_number(self):
		# Special error message for un-unique / empty matnumbers on user registration.
		data = self.cleaned_data['mat_number']
		if not data:
			raise forms.ValidationError("This field is required.")
		if User.objects.filter(mat_number=data):
			admins = map(lambda user: "<a href='mailto:%s'>%s</a>" % (user.email, user.get_full_name()), User.objects.filter(is_superuser=True))
			admins = reduce(lambda x,y: x + ', ' + y, admins)
			raise forms.ValidationError(mark_safe("A user with this number is allready registered. Please Contact an Administrator: %s" % admins	))
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
		use_https=False
		t = loader.get_template('registration/registration_email.html')
		c = {
			'email': user.email,
			'domain': settings.BASE_URL,
			'site_name': settings.SITE_NAME,
			'uid': int_to_base36(user.id),
			'user': user,
			'protocol': use_https and 'https' or 'http',
			'activation_key': activation_key,
			'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
			}
		send_mail(_("Account activation on %s") % site_name, t.render(Context(c)), None, [user.email])
		
		return user

class UserChangeForm(forms.ModelForm):
	
	# overriding modelfields to ensure required fields are provided
	first_name = forms.CharField(max_length = 30,required=True)
	last_name = forms.CharField(max_length = 30,required=True)
	#email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ("username","first_name","last_name")


	
class AdminUserCreationForm(UserBaseCreationForm):
	class Meta:
		model = User
		
class AdminUserChangeForm(UserBaseChangeForm):
	class Meta:
		model = User

	def clean(self):
		# Only if user is in group "User" require a mat number.
		cleaned_data = super(AdminUserChangeForm, self).clean()
		if ( cleaned_data.get("groups").filter(name="User") and not cleaned_data.get("mat_number")):
			self._errors["mat_number"] = self.error_class(["This field is required for Users."])
			del cleaned_data["mat_number"]
		return cleaned_data
