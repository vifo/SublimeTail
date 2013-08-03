# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view


class TailNewViewCommand(sublime_plugin.WindowCommand):

    """
    Sublime Text window command ``tail_new_view``.

    Opens a new Tail view with no sources configured.
    """

    def is_enabled(self):
        """
        Returns, whether command can be run this time.

        :returns:
            * ``True``, if plugin is enabled
            * ``False`` otherwise
        :rtype:
            *bool*
        """

        return plugin.is_enabled()

    def run(self, **kwargs):
        """
        Run command ``tail_new_view``.

        :returns: Nothing
        """

        sublime_view = self.window.new_file()
        get_tail_view(sublime_view=sublime_view, create=True)
        sublime.status_message('%s: No sources configured. Add with "Tail: Add File To Current View"' % (plugin.NAME))
