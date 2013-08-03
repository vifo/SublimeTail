# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view


class TailViewStopCommand(sublime_plugin.TextCommand):

    """
    Sublime Text text command ``tail_view_stop``.

    Stops tailing in a Tail view.
    """

    def is_enabled(self):
        """
        Reports, whether command can be run this time.

        :returns:
            * ``True``, if plugin is enabled, current view is a Tail view and
              view is running
            * ``False`` otherwise
        :rtype:
            *bool*
        """

        if not plugin.is_enabled():
            return False

        tail_view = get_tail_view(sublime_view=self.view)
        if not tail_view:
            return False

        return tail_view.is_running()

    def run(self, edit, **kwargs):
        """
        Run command ``tail_view_stop``.

        :returns:
            *Nothing*
        """

        tail_view = get_tail_view(sublime_view=self.view)
        if not tail_view:
            return False

        return tail_view.stop()
