# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view


class TailViewUpdateCommand(sublime_plugin.TextCommand):

    """
    Sublime Text text command ``tail_view_update``.

    Updates view with data from associated Tail view.
    """

    def run(self, edit, **kwargs):
        """
        Run command ``tail_view_update``.

        :returns:
            *Nothing*
        """

        sublime_view = self.view
        tail_view = get_tail_view(sublime_view=sublime_view)

        # tail_view.acquire_view_update_lock()
        while tail_view.has_lines():
            line = tail_view.shift_line()
            sublime_view.insert(edit, sublime_view.size(), line.line + "\n")
        sublime_view.show(sublime_view.size())

        # tail_view.release_view_update_lock()
