# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
from .. import plugin
from ..view import get_tail_view
from ..source import get_tail_source


class TailViewAddFileCommand(sublime_plugin.TextCommand):

    """
    Sublime Text text command ``tail_view_add_file``.

    Adds a file as additional source to an existing Tail view.
    """

    def is_enabled(self):
        """
        Returns, whether command can be run this time.

        :returns:
            * ``True``, if plugin is enabled and current view is a Tail view.
            * ``False`` otherwise
        :rtype:
            bool
        """

        if not plugin.is_enabled():
            return False

        tail_view = get_tail_view(sublime_view=self.view)
        return tail_view is not None

    def run(self, edit, **kwargs):
        """
        Run command ``tail_view_add_file``.

        :returns: Nothing
        """

        window = self.view.window()

        def on_done(filepath):
            plugin.log(plugin.LOG_TRACE, "tail_view_add_file.run.on_done() called. Result: %s" % (filepath))

            tail_view = get_tail_view(self.view)
            tail_source = get_tail_source(filepath=filepath)

            if not tail_view.has_source(source=tail_source):
                tail_view.add_source(tail_source)
                sublime.status_message('%s: Added "%s"' % (plugin.NAME, filepath))
            else:
                sublime.status_message('%s: Source "%s" already attached' % (plugin.NAME, filepath))

        window.show_input_panel("Add filepath:", "", on_done, None, None)
