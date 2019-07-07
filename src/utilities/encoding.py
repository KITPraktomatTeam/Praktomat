# -*- coding: utf-8 -*-

import chardet
import re

def get_unicode(bytestring):
    from six import PY2
    if bytestring:
        """ Returns guessed unicode representation of file content. """
        if PY2:
            if isinstance(bytestring, unicode):
                return bytestring
        else:
            if isinstance(bytestring, str):
                return bytestring


        # Treat any 8-bit ASCII extension as latin1/western european
        charset = chardet.detect(bytestring)["encoding"]
        if charset:
            charset = re.sub(r"ISO-8859-[0-9]", "ISO-8859-1", charset)
        if charset:
            charset = re.sub(r"windows-125[01235]", "ISO-8859-1", charset)

        for chset in ["utf-8", charset, "ISO-8859-1"]:
            if chset:
                try:
                    return bytestring.decode(chset)
                except UnicodeDecodeError:
                    pass
                except LookupError:
                    pass
        raise UnicodeDecodeError("Unable to detect proper characterset")
    else:
        if PY2:
            return u''
        else:
            return ''

def get_utf8(unicodestring):
    return unicodestring.encode("utf-8")
