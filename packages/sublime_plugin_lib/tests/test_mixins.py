# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys

from ..mock import sublime
sys.modules['sublime'] = sublime
from .. import mixins
from ..mixins import enhance_sublime_view


def test_enhance_sublime_view():
    class MyView(object):
        pass

    v = MyView()
    v = enhance_sublime_view(v)
    assert isinstance(v, MyView)

    for k in [
        'append',
        'remove_trailing_newlines',
        'replace_contents',
    ]:
        assert hasattr(v, k)
