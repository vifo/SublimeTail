# -*- coding: utf-8 -*-

"""
Compatibility module for running `Sublime Text` plugins under Python 2.6+ and
Python 3.x+ at the same time.

Basically a cut down version of

    https://pypi.python.org/pypi/six

with features we really need, when running under `Sublime Text`.
"""

from __future__ import print_function, unicode_literals
import sys

__all__ = [
    'PY2',
    'PY3',
    'WindowsError',
]

PY3 = sys.version_info[0] == 3      #: ``True``, if running under Python 3, ``False`` otherwise.
PY2 = sys.version_info[0] == 2      #: ``True``, if running under Python 2, ``False`` otherwise.

if PY3:
    binary_type = bytes
    integer_types = (int)
    list_types = (list)
    string_types = (str)
    text_type = str
else:
    binary_type = str
    integer_types = (int, long)
    list_types = (list)
    string_types = (basestring)
    text_type = unicode

# Create null WindowsError exception on non-Windows platforms.
try:
    from exceptions import WindowsError
except (ImportError):
    class WindowsError(Exception):
        pass
