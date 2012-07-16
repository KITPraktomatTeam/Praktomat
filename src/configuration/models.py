from django.db import models
from datetime import date

class Settings(models.Model):
	""" Singleton object containing site wide settings confiurale by the trainer. """
	
	class Meta:
		# Django admin adds an 's' to the class name; prevent SettingSS
		verbose_name = 'Setting'
	
	email_validation_regex = models.CharField(max_length=200, blank=True, default=".*@(student.)?kit.edu", help_text="Regular expression used to check the email domain of registering users.")
	mat_number_validation_regex = models.CharField(max_length=200, blank=True, default="\d{5,7}", help_text="Regular expression used to check the student number.")
	deny_registration_from = models.DateTimeField(default=date(2222, 01, 01), help_text="After this date, registration wont be possible.")
	acount_activation_days = models.IntegerField(default=10, help_text="Days until the user has time to activate his account with the link send in the registation email.")
	
	account_manual_validation = models.BooleanField(default=False, help_text="If enabled, registrations via the website must be manually validate by a trainer.")

	accept_all_solutions = models.BooleanField(default=False, help_text="If enabled, solutions with required checkers, which are not passed, can become the final soution.")
	
	anonymous_attestation = models.BooleanField(default=False, help_text="If enabled, the tutor can't see the name of the user, who subbmitted the solution.")

	final_grades_published = models.BooleanField(default=False, help_text="If enabeld, all users can see their final grades.")

class Chunk(models.Model):
	""" A Chunk is a piece of content associated with a unique key that can be inserted into any template with the use of a special template tag """
	settings = models.ForeignKey(Settings, default=1, help_text="Makes it easy to display chunks as inlines in Settings.")
	key = models.CharField(help_text="A unique name for this chunk of content", blank=False, max_length=255, unique=True, editable=False)
	content = models.TextField(blank=True)
	
	def __unicode__(self):
		return u"%s" % (self.key,)
