from django.core.management.base import NoArgsCommand, CommandError
from accounts.models import User

from os.path import join, dirname as dir

class Command(NoArgsCommand):
	help = 'Delete all users which have not activated their account.'
	
	def handle_noargs(self, **options):
		count = 0
		for user in User.objects.all():
			if not user.is_activated() and user.activation_key_expired():
				user.delete()
				count += 1
		print "%i users have been deleted." % count


