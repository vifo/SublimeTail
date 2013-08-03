# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view
from ..source import get_tail_source


class TailViewRemoveFileCommand(sublime_plugin.TextCommand):

    """
    Sublime Text text command ``tail_view_remove_file``.

    Remove a file from an an existing Tail view.
    """

    def is_enabled(self):
        """
        Returns, whether command can be run this time.

        :returns:
            * ``True``, if plugin is enabled, current view is a Tail view and
              has one or more sources attached.
            * ``False`` otherwise
        :rtype:
            *bool*
        """

        if not plugin.is_enabled():
            return False

        tail_view = get_tail_view(sublime_view=self.view)
        if tail_view is None:
            return False

        return tail_view.has_sources()

    def run(self, edit, **kwargs):
        """
        Run command ``tail_view_add_file``.

        :returns:
            *Nothing*
        """

        sublime.error_message('This command is not implemented yet.')
