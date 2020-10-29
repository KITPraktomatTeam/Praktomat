from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Delete users which have not activated their account. Users registered via Shibboleth are ignored.'

    def handle(self, *args, **options):
        count = 0
        for user in User.objects.all():
            if user.activation_key != "" and not user.is_activated() and user.activation_key_expired():
                user.delete()
                count += 1
        self.stdout.write("%i users have been deleted." % count)
