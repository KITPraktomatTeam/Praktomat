# -*- coding: utf-8 -*-

import chardet
	
def get_unicode(bytestring):
	""" Returns guessed unicode representation of file content. """
	return bytestring.decode(chardet.detect(bytestring)["encoding"])

def get_utf8(unicodestring):
	return unicodestring.encode("utf-8")