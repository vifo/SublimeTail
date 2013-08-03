# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view


class TailViewStartCommand(sublime_plugin.TextCommand):

    """
    Sublime Text text command ``tail_view_start``.

    Starts tailing in a Tail view. Buffer contents will be preserved and
    configured sources will be tailed from their current position.
    """

    def is_enabled(self):
        """
        Reports, whether command can be run this time.

        :returns:
            * ``True``, if plugin is enabled, current view is a Tail view and
              view is stopped
            * ``False`` otherwise
        :rtype:
            *bool*
        """

        if not plugin.is_enabled():
            return False

        tail_view = get_tail_view(sublime_view=self.view)
        if not tail_view:
            return False

        return tail_view.is_stopped()

    def run(self, edit, **kwargs):
        """
        Run command ``tail_view_start``.

        :returns:
            *Nothing*
        """

        tail_view = get_tail_view(sublime_view=self.view)
        if not tail_view:
            return False

        return tail_view.start()
