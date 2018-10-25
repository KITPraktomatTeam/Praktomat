"""
Management utility to make a super a superuser.
"""

import re
import sys
from optparse import make_option
from django.contrib.auth.models import User
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

class Command(BaseCommand):
	help = 'Make a user a superuser.'

	def add_arguments(self, parser):
		parser.add_argument('--username', dest='username', default=None,
                        help='Specifies the username of the existing user (mail address for shibboleth users).')

	def handle(self, *args, **options):
		username = options.get('username', None)
		verbosity = int(options.get('verbosity', 1))

		if not username:
			raise CommandError("Please specify a user with --username")	

		user = User.objects.get(username=username)
		if verbosity >= 1:
		  self.stdout.write("Found user %s\n" % user)
		user.is_staff = True
		user.is_active = True
		user.is_superuser = True
		user.save()
		if verbosity >= 1:
		  self.stdout.write("Superuser created successfully.\n")

