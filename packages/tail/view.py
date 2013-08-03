# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
import threading
import re
from ..sublime_plugin_lib import compat
from . import plugin

# Registered Tail views.
TAIL_VIEWS = {}


def destroy_tail_view(sublime_view, **kwargs):
    global TAIL_VIEWS

    if not isinstance(sublime_view, sublime.View):
        raise ValueError('Argument "sublime_view" must be a sublime.View object')

    # Check, if given Sublime view has an associated Tail view. If yes,
    # cleanup.
    sublime_view_id = sublime_view.id()
    if sublime_view_id in TAIL_VIEWS:
        TAIL_VIEWS[sublime_view_id].destroy()
        del TAIL_VIEWS[sublime_view_id]


def get_tail_view(sublime_view, create=False, **kwargs):
    global TAIL_VIEWS

    if not isinstance(sublime_view, sublime.View):
        raise ValueError('Argument "sublime_view" must be a sublime.View object')

    # Check, if we already have a Tail view for given Sublime view. If not,
    # create one and register it in list of Tail views.
    sublime_view_id = sublime_view.id()

    if sublime_view_id not in TAIL_VIEWS:
        if create:
            TAIL_VIEWS[sublime_view_id] = TailView(sublime_view, **kwargs)
            TAIL_VIEWS[sublime_view_id].init()
        else:
            return None

    return TAIL_VIEWS[sublime_view_id]


def is_tail_view(sublime_view, **kwargs):
    global TAIL_VIEWS

    if not isinstance(sublime_view, sublime.View):
        raise ValueError('Argument "sublime_view" must be a sublime.View object')

    # Check, if given Sublime view is a Tail view.
    sublime_view_id = sublime_view.id()
    return sublime_view_id in TAIL_VIEWS


class TailView(object):

    """
    Class representing a tail view with internal buffer and separate update
    thread.
    """

    STATE_STOPPED = 0
    STATE_PAUSED = 1
    STATE_RUNNING = 2

    def __init__(self, sublime_view, **kwargs):
        self.sublime_view = sublime_view
        self.sublime_view_update_lock = threading.Lock()
        self.sources = {}
        self.lines = []
        self.lines_lock = threading.Lock()
        self.filter = None
        self.state = self.STATE_STOPPED

    def add_line(self, line):
        """
        Add ``line`` to this view. If a filter is set, the line will only be
        added, if it matches the filter.

        :param line: Line to be added
        :type line: ``TailSourceLine``
        """

        if self.state == self.STATE_STOPPED:
            return

        if self.filter is not None:
            if not self.filter.match(line.line):
                return

        self.lines_lock.acquire()
        self.lines.append(line)
        if len(self.lines) > 500:
            self.lines.pop(0)
        self.lines_lock.release()

        # Update view.
        sublime.set_timeout(lambda: self.sublime_view.run_command('tail_view_update'), 0)

    def acquire_view_update_lock(self):
        return self.sublime_view_update_lock.acquire()

    def add_source(self, source):
        """
        Add ``source`` to this view.
        """

        if not self.has_source(source):
            self.sources[id(source)] = source
            source.attach_to_view(self)
            self.update_name()
            return True
        else:
            return False

    def destroy(self):
        self.remove_all_sources()

    def has_source(self, source):
        """
        Checks, if ``source`` is already attached to this view.

        :returns:
            * ``True``, if source is attached to this view
            * ``False`` otherwise
        :rtype:
            *bool*
        """
        return id(source) in self.sources

    def init(self):
        view = self.sublime_view
        view.set_scratch(True)
        view.settings().set('spell_check', False)
        self.update_name()

    def get_filter(self):
        """
        Return current filter as compiled regular expression. Returns
        ``None``, if no filter has been set yet.
        """

        return self.filter

    def get_state(self):
        return self.state

    def has_lines(self):
        """
        Return ``True``, if this view has new lines in buffer, ``False``
        otherwise.
        """

        return len(self.lines) > 0

    def has_sources(self):
        """
        Return ``True``, if this view has attached sources, ``False``
        otherwise.
        """

        return len(self.sources) > 0

    def is_paused(self):
        """
        Returns ``True``, if view is currently paused, ``False`` otherwise.
        """

        return self.state == self.STATE_PAUSED

    def is_running(self):
        """
        Returns ``True``, if view is currently running, ``False`` otherwise.
        """

        return self.state == self.STATE_RUNNING

    def is_stopped(self):
        """
        Returns ``True``, if view is currently stopped, ``False`` otherwise.
        """

        return self.state == self.STATE_STOPPED

    def release_view_update_lock(self):
        return self.sublime_view_update_lock.relase()

    def remove_source(self, source):
        """
        Remove ``source`` from this view.
        """

        if id(source) in self.sources:
            source.detach_from_view(self)
            del self.sources[id(source)]
            self.update_name()

    def remove_all_sources(self):
        """
        Detach all sources from view and remove them.
        """

        for source in self.sources.values() if compat.PY3 else self.sources.itervalues():
            source.detach_from_view(self)
        self.sources = {}
        self.update_name()

    def start(self):
        if self.state in [self.STATE_STOPPED, self.STATE_PAUSED]:
            self.state = self.STATE_RUNNING
            sublime.status_message('%s: Started tailing' % (plugin.NAME))
            self.update_name()
        return True

    def set_filter(self, filter):
        """
        Set new filter. ``filter`` must be a add_source regular expression.
        """

        self.filter = re.compile(filter)

    def shift_line(self):
        """
        Shift first available line from buffer.
        """

        if not len(self.lines):
            return None

        # TODO: Check, if the lock is really needed here. Is .pop() thread
        # safe?
        self.lines_lock.acquire()
        line = self.lines.pop(0)
        self.lines_lock.release()

        return line

    def stop(self):
        if self.state in [self.STATE_RUNNING, self.STATE_PAUSED]:
            self.state = self.STATE_STOPPED
            sublime.status_message('%s: Stopped tailing' % (plugin.NAME))
            self.update_name()
        return True

    def update_name(self):
        if not self.has_sources():
            self.sublime_view.set_name('%s: <No Sources>' % (plugin.NAME))
        else:
            filenames = []
            for source in self.sources.values() if compat.PY3 else self.sources.itervalues():
                filenames.append(source.get_filename())
                if len(filenames) >= 3:
                    break

            if len(self.sources) >= 4:
                filenames.append('%d other(s)' % (len(self.sources) - 3))
            filenames = '; '.join(filenames)

            self.sublime_view.set_name('%s: %s' % (plugin.NAME, filenames))


class TailViewCloseListener(sublime_plugin.EventListener):

    def on_close(self, sublime_view):
        if is_tail_view(sublime_view):
            destroy_tail_view(sublime_view)
