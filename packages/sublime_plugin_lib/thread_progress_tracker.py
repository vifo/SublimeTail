# -*- coding: utf-8 -*-

"""
Thread progress tracker for `Sublime Text`. Taken from:

    https://github.com/wbond/sublime_package_control

and adapted slightly. Example usage::

    from sublime_plugin_lib.thread_progress_tracker import ThreadProgressTracker

    thread = ...
    thread.start()
    tracker = ThreadProgressTracker(thread=thread)
"""

from __future__ import print_function, unicode_literals
import sublime


class ThreadProgressTracker():

    """
    Animates an indicator, [=   ], in the status area while a thread runs

    :param thread:
        The thread to track for activity

    :param message:
        The message to display next to the activity indicator

    :param done_message:
        The message to display once the thread is complete
    """

    def __init__(self, thread, message, done_message):
        self.thread = thread
        self.message = message
        self.done_message = done_message
        self.addend = 1
        self.size = 8
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            if hasattr(self.thread, 'result') and not self.thread.result:
                sublime.status_message('')
            else:
                sublime.status_message(self.done_message)

            return

        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message('%s [%s=%s]' % (self.message, ' ' * before, ' ' * after))

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 100)
