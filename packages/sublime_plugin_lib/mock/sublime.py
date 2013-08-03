# -*- coding: utf-8 -*-

"""
Fake ``sublime`` module with minimal functionality for testing code outside of
`Sublime Text`.
"""

from __future__ import print_function, unicode_literals
import sys
import threading
import time

_status_message = None


def get_status_message():
    """
    Get current status message.

    :returns: Current status message.
    :rtype: string

    >>> sublime.status_message("SomePlugin: working hard")
    >>> sublime.get_status_message()
    'SomePlugin: working hard'
    """

    global _status_message
    return _status_message


def platform():
    """
    Returns current platform.

    :returns: Platform, which may be "osx", "linux" or "windows".
    :rtype: string

    >>> sublime.platform()
    'linux'
    """

    if sys.platform.startswith('win'):
        return 'windows'

    return 'linux'


def set_timeout(callback, delay):

    class MyThread(threading.Thread):

        def __init__(self, delay=1000, callback=None):
            self.delay = delay
            self.callback = callback
            threading.Thread.__init__(self)

        def run(self):
            time.sleep(self.delay / 1000)
            if self.callback is not None:
                self.callback()

    t = MyThread(callback=callback, delay=delay)
    t.start()


def status_message(string):
    """
    Set status message.

    :param string: Message to be displayed.
    :type string: string

    >>> sublime.status_message("SomePlugin: working hard")
    >>> sublime.get_status_message()
    'SomePlugin: working hard'
    """

    global _status_message
    _status_message = string


class Region(object):

    """
    Fake ``Region`` class.
    """
