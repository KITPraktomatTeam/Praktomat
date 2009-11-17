import datetime
import re

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	activation_key=models.CharField(_('activation key'), max_length=40, editable=False)
	
	#ACTIVATED = u"ALREADY_ACTIVATED"
	
	def activation_key_expired(self):
		"""
		Determine whether the activation key has expired, returning a boolean 
		-- ``True`` if the key has expired.
		
		Key expiration is determined by a two-step process:
		
		1. 	If the user has already activated, the key will have been
			reset to the string ``ALREADY_ACTIVATED``. Re-activating is
			not permitted, and so this method returns ``True`` in this
			case.
			
		2. 	Otherwise, the date the user signed up is incremented by
			the number of days specified in the setting
			''ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
			days after signup during which a user is allowed to
			activate their account); if the result is less than or
			equal to the current date, the key has expired and this
			method returns ``True``.
		"""
		expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
		return self.activation_key == u"ALREADY_ACTIVATED" or \
			(self.user.date_joined + expiration_date <= datetime.datetime.now())
	activation_key_expired.boolean = True
	
	def activate_user(activation_key):
		"""
		Validate an activation key and activate the corresponding
		''User`` if valid.
		
		If the key is valid and has not expired, return the ``User``
		after activating.
		
		If the key is not valid or has expired, return ``False``.
		
		If the key is valid but the ``User`` is already active,
		return ``False``.
		
		To prevent reactivation of an account which has been
		deactivated by site administrators, the activation key is
		reset to the string ``ALREADY_ACTIVATED`` after successful
		activation.
		
		"""
		# Make sure the key we're trying conforms to the pattern of a
		# SHA1 hash; if it doesn't, no point trying to look it up in
		# the database.
		SHA1_RE = re.compile('^[a-f0-9]{40}$')
		if SHA1_RE.search(activation_key):
			try:
				profile = UserProfile.objects.get(activation_key=activation_key)
			except UserProfile.DoesNotExist:
				return False
			if not profile.activation_key_expired():
				user = profile.user
				user.is_active = True
				user.save()
				profile.activation_key = u"ALREADY_ACTIVATED"
				profile.save()
				return user
			return False
	activate_user = staticmethod(activate_user)
	
	# The rest is completely up to you...
	mat_number = models.IntegerField()
	degree_course = models.CharField(max_length=30)
