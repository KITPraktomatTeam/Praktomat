# -*- coding: utf-8 -*-

import chardet
import re
	
def get_unicode(bytestring):
	""" Returns guessed unicode representation of file content. """
	return bytestring.decode(re.sub(r"ISO-8859-[0-9]","ISO-8859-1",chardet.detect(bytestring)["encoding"]))

def get_utf8(unicodestring):
	return unicodestring.encode("utf-8")
