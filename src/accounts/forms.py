import datetime
import random
import hashlib
import re

from django.conf import settings
from django.db import models, transaction
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import UserCreationForm as UserBaseCreationForm, UserChangeForm as UserBaseChangeForm
from django.core.mail import send_mail
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe
from configuration import get_settings

from accounts.models import User

class MyRegistrationForm(UserBaseCreationForm):
	
	def __init__(self, *args, **kwargs):
		# post, domaine=None, use_https=None):
		if 'domain' in kwargs:
			self.domain = kwargs.pop('domain')
		if 'use_https' in kwargs:
			self.use_https = kwargs.pop('use_https')
		super(MyRegistrationForm, self).__init__(*args, **kwargs)
	
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
		email_validation_regex = get_settings().email_validation_regex
		if email_validation_regex and not re.match(email_validation_regex, data):
			raise forms.ValidationError("The email you have provided is not valid. It has to be in: " + email_validation_regex)	
		return data

	def clean_mat_number(self):
		# Special error message for un-unique / empty matnumbers on user registration.
		data = self.cleaned_data['mat_number']
		if not data:
			raise forms.ValidationError("This field is required.")
		for user in User.objects.filter(mat_number=data):
			if user.is_activated():
				trainers = map(lambda user: "<a href='mailto:%s'>%s</a>" % (user.email, user.get_full_name() or user.email), Group.objects.get(name='Trainer').user_set.all())
				trainers = ', '.join(trainers)
				raise forms.ValidationError(mark_safe("A user with this number is already registered. Please Contact an Trainer: %s" % trainers ))
		return data


	@transaction.atomic
	def save(self):
		user = super(MyRegistrationForm, self).save()
		
		# default group: user
		user.groups = Group.objects.filter(name='User')
		 
		# disable user until activated via email
		user.is_active=False
		
		user.set_new_activation_key()

		user.mat_number=self.cleaned_data.get("mat_number")
		
		user.save()
		
		# Send activation email
		c = {
			'email': user.email,
			'domain': self.domain,
			'site_name': settings.SITE_NAME,
			'uid': int_to_base36(user.id),
			'user': user,
			'protocol': self.use_https and 'https' or 'http',
			'activation_key': user.activation_key,
			'expiration_days': get_settings().acount_activation_days,
			}

		if get_settings().account_manual_validation:
			t = loader.get_template('registration/registration_email_manual_to_staff.html')
 			send_mail(_("Account activation on %s for %s (%s) ") % (settings.SITE_NAME,user.username,unicode(user)), t.render(c), None, [staff.email for staff in User.objects.all().filter(is_staff=True)])

			t = loader.get_template('registration/registration_email_manual_to_user.html')
 			send_mail(_("Account activation on %s") % settings.SITE_NAME, t.render(c), None, [user.email])
		else:
			t = loader.get_template('registration/registration_email.html')
			send_mail(_("Account activation on %s") % settings.SITE_NAME, t.render(c), None, [user.email])
		
		return user

class UserChangeForm(forms.ModelForm):
	
	# overriding modelfields to ensure required fields are provided
	first_name = forms.CharField(max_length = 30,required=True)
	last_name = forms.CharField(max_length = 30,required=True)
	#email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ("first_name","last_name")


class AdminUserCreationForm(UserBaseCreationForm):
	class Meta:
		model = User
                fields = "__all__"


class AdminUserChangeForm(UserBaseChangeForm):
	class Meta:
		model = User
                fields = "__all__"

	def clean(self):
		# Only if user is in group "User" require a mat number.
		cleaned_data = super(AdminUserChangeForm, self).clean()
		groups = cleaned_data.get("groups")
		if not groups:
			self._errors["groups"] = self.error_class(["This field is required."])
		if ( groups and groups.filter(name="User") and not cleaned_data.get("mat_number")):
			self._errors["mat_number"] = self.error_class(["This field is required for Users."])
			if "mat_number" in cleaned_data:
				#mat_number was probably removed prior to this validation (eg. no number)
				del cleaned_data["mat_number"]
		return cleaned_data


reactivation_message_text = """ {% autoescape off %}
You're receiving this e-mail because you have been registerd at {{ site_name }}.

Please go to the following page to activate your account within {{ expiration_days }} days.

{{ protocol }}://{{ domain }}{% url registration_activate activation_key=activation_key %}

Your username, in case you've forgotten: {{ user.username }}

Thanks for using our site!

The {{ site_name }} team

{% endautoescape %} """

class ImportForm(forms.Form):
	file = forms.FileField(required=True, help_text = "The file exported from the list view. Allready existing users will be ignorred.")
	require_reactivation = forms.BooleanField(initial=True, required=False, help_text = "Deactivate all imported users")
	send_reactivation_email = forms.BooleanField(initial=False, required=False, help_text = "Send activation email to imported users (if deactivated during import)")
	meassagetext = forms.CharField(required=False, widget=forms.Textarea, initial = reactivation_message_text, help_text = "Message to be embedded into activation mail if reactivation is required.")

class ImportTutorialAssignmentForm(forms.Form):
	csv_file = forms.FileField(required=True, help_text = "The csv file containing the tutorial name and the students mat number.")
	delimiter = forms.CharField(required=True, max_length = 1, initial = ";", help_text = "A one-character string used to separate fields.")
	quotechar = forms.CharField(required=True, max_length = 1, initial = "|", help_text = "A one-character string used to quote fields.")
	name_coloum = forms.IntegerField(required=True, initial = 0, help_text = "The index of the field containing the name of the tutorial.")
	mat_coloum = forms.IntegerField(required=True, initial = 1, help_text = "The index of the field containing the mat number of the user.")
	
	

class ImportMatriculationListForm(forms.Form):
    mat_number_file = forms.FileField(required=True, help_text = "A text file consisting of one matriculatoin number per line.")
    remove_others = forms.BooleanField(required=False, initial = True, help_text = "Also remove all users from the group if they are not listed here.")
    create_users = forms.BooleanField(required=False, initial = False, help_text = "If a matriculation number is not known yet, create a stub user object")
