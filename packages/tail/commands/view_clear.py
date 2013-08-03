# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view


class TailViewClearCommand(sublime_plugin.TextCommand):

    """
    Sublime Text text command ``tail_view_clear``.

    Clear contents of existing Tail view.
    """

    def is_enabled(self):
        """
        Reports, whether command can be run this time.

        :returns:
            * ``True``, if plugin is enabled, current view is a Tail view
            * ``False`` otherwise
        :rtype:
            *bool*
        """

        if not plugin.is_enabled():
            return False

        tail_view = get_tail_view(sublime_view=self.view)
        return tail_view is not None

    def run(self, edit, **kwargs):
        """
        Run command ``tail_view_clear``.

        :returns:
            *Nothing*
        """

        tail_view = get_tail_view(sublime_view=self.view)
        if not tail_view:
            return False

        self.view.erase(edit, sublime.Region(0, self.view.size()))
