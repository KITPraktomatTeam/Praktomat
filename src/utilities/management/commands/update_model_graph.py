from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import models

from os.path import join, dirname as dir
import shutil
import tempfile

class Command(BaseCommand):
	help = 'Updates the vector images in documentation/modelgraph. Requires instalation of graphviz and pygraphviz.'

	def handle_noargs(self, **options):
			export_folder = join(dir(dir(dir(dir(dir(__file__))))),"documentation","model_graph")
			management.call_command('graph_models', 'tasks', outputfile=join(export_folder,'tasks.svg'))
			management.call_command('graph_models', 'tasks', outputfile=join(export_folder,'tasks.gif'))
			management.call_command('graph_models', 'solutions', outputfile=join(export_folder,'solutions.svg'))
			management.call_command('graph_models', 'solutions', outputfile=join(export_folder,'solutions.gif'))
			management.call_command('graph_models', 'attestation', outputfile=join(export_folder,'attestation.svg'))
			management.call_command('graph_models', 'attestation', outputfile=join(export_folder,'attestation.gif'))
			management.call_command('graph_models', 'accounts', outputfile=join(export_folder,'accounts.svg'))
			management.call_command('graph_models', 'accounts', outputfile=join(export_folder,'accounts.gif'))
			management.call_command('graph_models', 'checker', outputfile=join(export_folder,'checker.svg'))
			management.call_command('graph_models', 'checker', outputfile=join(export_folder,'checker.gif'))
			management.call_command('graph_models', 'tasks', 'solutions', 'attestation', 'accounts', group_models = True, disable_fields = True, outputfile=join(export_folder,'overview.svg'))
			management.call_command('graph_models', 'tasks', 'solutions', 'attestation', 'accounts', group_models = True, disable_fields = True, outputfile=join(export_folder,'overview.gif'))
			management.call_command('graph_models', all_applications = True, group_models = True, outputfile=join(export_folder,'extended_overview.svg'))
			management.call_command('graph_models', all_applications = True, group_models = True, outputfile=join(export_folder,'extended_overview.gif'))
			print 'Successfully updated model graph.'
		
