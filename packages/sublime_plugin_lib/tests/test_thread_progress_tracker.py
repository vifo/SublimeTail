# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys
import threading
import time

from ..mock import sublime, sublime_plugin
sys.modules['sublime'] = sublime
sys.modules['sublime_plugin'] = sublime_plugin
from .. import thread_progress_tracker
from ..thread_progress_tracker import ThreadProgressTracker


def test_thread_progress_tracker():

    class MyThread(threading.Thread):

        def __init__(self, **kwargs):
            threading.Thread.__init__(self)

        def run(self):
            time.sleep(1.0)

    thread = MyThread()
    thread.start()

    tracker = ThreadProgressTracker(
        thread=thread, message='SublimePluginLib: working', done_message='SublimePluginLib: done')
    assert isinstance(tracker, ThreadProgressTracker)

    # Wait for status to change
    time.sleep(0.5)
    assert sublime.get_status_message().startswith('SublimePluginLib: working')

    time.sleep(1.0)
    assert sublime.get_status_message() == 'SublimePluginLib: done'
