# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys
from ..mock import sublime, sublime_plugin
sys.modules['sublime'] = sublime
sys.modules['sublime_plugin'] = sublime_plugin
from ..signal import Signal


def test_tbd():
    pass
