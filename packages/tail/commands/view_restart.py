# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view


class TailViewRestartCommand(sublime_plugin.TextCommand):

    """
    Sublime Text text command ``tail_view_restart``.

    Restart tailing in an existing view. This will clear the buffer and start
    tailing configured sources.
    """

    def is_enabled(self):
        """
        Reports, whether command can be run this time.

        :returns:
            * ``True``, if plugin is enabled, current view is a Tail view and
              view is paused or stopped.
            * ``False`` otherwise
        :rtype:
            *bool*
        """

        if not plugin.is_enabled():
            return False

        tail_view = get_tail_view(sublime_view=self.view)
        if not tail_view:
            return False

        return tail_view.is_stopped() or tail_view.is_paused()

    def run(self, edit, **kwargs):
        """
        Run command ``tail_view_restart``.

        :returns:
            *Nothing*
        """

        tail_view = get_tail_view(sublime_view=self.view)
        if not tail_view:
            return False

        self.view.erase(edit, sublime.Region(0, self.view.size()))
        return tail_view.start()
