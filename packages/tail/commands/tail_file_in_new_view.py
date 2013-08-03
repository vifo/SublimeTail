# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view, is_tail_view
from ..source import get_tail_source


class TailTailFileInNewView(sublime_plugin.TextCommand):

    """
    Sublime Text text command ``tail_tail_file_in_new_view``.

    Opens a new Tail view with current file as only source.
    """

    def is_enabled(self, **kwargs):
        """
        Reports, whether command can be run this time.

        :returns:
            * ``True``, if plugin is enabled and current view has a physical
              file associated.
            * ``False`` otherwise
        :rtype:
            *bool*
        """

        if not plugin.is_enabled():
            return False

        # Determine caller. Can be called from view or side bar.
        caller = kwargs['caller'] if 'caller' in kwargs else 'view'
        if caller not in ['view', 'sidebar']:
            caller = 'view'

        # If called from the sidebar, the view might report a wrong
        # file_name(), or even none. Let run() handle this.
        if caller == 'sidebar':
            return True

        # Not available, if this is already a Tail view.
        if is_tail_view(self.view):
            return False

        # We need a physical file.
        if self.view.file_name() is None:
            return False

        return True

    def run(self, edit, **kwargs):
        """
        Run command ``tail_tail_file_in_new_view``.

        :returns:
            *Nothing*
        """

        if not plugin.is_enabled():
            return False

        # We need a physical file.
        filename = self.view.file_name()
        if filename is None:
            return False

        # Open new view, associate with a Tail view and add current file as
        # source.
        sublime_view = self.view.window().new_file()
        tail_view = get_tail_view(sublime_view=sublime_view, create=True)
        tail_view.add_source(get_tail_source(filepath=filename))
        tail_view.start()
