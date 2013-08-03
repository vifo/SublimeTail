# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys

from ...sublime_plugin_lib.mock import sublime, sublime_plugin
sys.modules['sublime'] = sublime
sys.modules['sublime_plugin'] = sublime_plugin


def test_import():
    from ..commands.new_view import TailNewViewCommand
    from ..commands.tail_file_in_new_view import TailTailFileInNewView
    from ..commands.view_add_file import TailViewAddFileCommand
    from ..commands.view_clear import TailViewClearCommand
    from ..commands.view_restart import TailViewRestartCommand
    from ..commands.view_start import TailViewStartCommand
    from ..commands.view_stop import TailViewStopCommand
    from ..commands.view_update import TailViewUpdateCommand
    from ..view import destroy_tail_view, get_tail_view, is_tail_view, TailView, TailViewCloseListener
    from ..source import get_tail_source, TailSource, TailSourceLine, TailSourceUpdater
    from ..plugin import get_log_level, get_setting, is_enabled, log
