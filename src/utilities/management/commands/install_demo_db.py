from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from os.path import join, dirname as dir
import shutil
import tempfile

class Command(BaseCommand):
	help = 'Copies the demo database into the application support folder'

	def handle_noargs(self, **options):
	   	try:
		   	application_support_folder = settings.UPLOAD_ROOT
		   	demo_support_folder = join(dir(dir(dir(dir(dir(dir(__file__)))))),"examples","PraktomatSupport")
		   	
		   	# create a backup
		   	archive_name = join(tempfile.gettempdir(), 'backup')
		   	archive_name = shutil.make_archive(archive_name, 'zip', application_support_folder)
		   	
		   	# delete old app support folder
		   	shutil.rmtree(application_support_folder)
	
		   	# copy demo files
		   	shutil.copytree(demo_support_folder, application_support_folder)
		   	
		   	# copy backup
		   	shutil.copy(archive_name, application_support_folder)
		   	
		   	print 'Successfully installed demo files and database. Backup of old files in "%s"' % join(application_support_folder, 'backup.zip')
	  	
		except:
			raise CommandError('An ERROR occurred. A backup of your files can be found here: ' % archive_name)

		