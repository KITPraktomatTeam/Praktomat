# -*- coding: utf-8 -*-

import string, os
from praktomat.utilities import encoding

def copy_processed_file(input_file_path, output_file_directory, environment):
	
	with open(input_file_path) as input_file:
		input_file_content = encoding.get_unicode(input_file.read())
	
	output_file_path = os.path.join(output_file_directory, os.path.basename(input_file.name))
	with open(output_file_path, 'w') as output_file:
		output_file.write(encodig.get_utf8(process_text(input_file_content, environment)))
	
def process_text(text, environment):
	if not environment.program():
		return text
	return text.replace(u'PROGRAM', environment.program())
	
	
	
#	# For security reasons, we disable a number of GNU M4 macros that might otherwise be used to gain file access.
#	undefine = ['-Ubuiltin', '-Uinclude', '-Usinclude', '-Usyscmd', '-Uesyscmd', '-Udivert', '-Uundivert', '-Udebugfile']
#	
#	if environment:
#		define = ['-DPROGRAM='+enironment.]
#	
#	args = ['m4'] + undefine + define + [file]
#	output = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=env.tmpdir()).communicate()[0]
	

 