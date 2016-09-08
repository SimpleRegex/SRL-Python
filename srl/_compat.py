# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2
_identity = lambda x: x

if PY2:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
else:
    text_type = str
    string_types = (str,)
    integer_types = (int,)
