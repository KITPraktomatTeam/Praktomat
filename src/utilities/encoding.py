# -*- coding: utf-8 -*-

import chardet
import re
	
def get_unicode(bytestring):
	if bytestring:
		""" Returns guessed unicode representation of file content. """

		# Treat any 8-bit ASCII extension as latin1/western european
		charset = chardet.detect(bytestring)["encoding"]
		charset = re.sub(r"ISO-8859-[0-9]","ISO-8859-1",charset)
		charset = re.sub(r"windows-125[01235]","ISO-8859-1",charset)

		return bytestring.decode(charset)
	else:
		return u''

def get_utf8(unicodestring):
	return unicodestring.encode("utf-8")
