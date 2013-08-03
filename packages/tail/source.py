# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import os
import sys
import threading
import time
from ..sublime_plugin_lib import compat
from . import plugin

# Registered Tail sources.
TAIL_SOURCES = {}


def get_tail_source(filepath, **kwargs):
    global TAIL_SOURCES

    # Check, if we already have a tail source for given filepath. If yes,
    # return it, otherwise create new source.
    if filepath not in TAIL_SOURCES:
        TAIL_SOURCES[filepath] = TailSource(filepath, **kwargs)
    return TAIL_SOURCES[filepath]


class TailSource(object):

    """
    Class representing a single tail source.
    """

    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.options = kwargs
        self.updater = None
        self.views_lock = threading.Lock()
        self.views = {}

    def add_line(self, line):
        """
        Add new line. Called by thread following physical source.
        """

        self.views_lock.acquire()

        for view in self.views.values():
            view.add_line(line)

        self.views_lock.release()

    def attach_to_view(self, view):
        """
        Attach this source to a view.
        """

        self.views_lock.acquire()

        if id(view) not in self.views:
            self.views[id(view)] = view
        start_updater = self.is_attached()

        self.views_lock.release()

        if start_updater:
            self.start_updater()

    def detach_from_view(self, view):
        """
        Detached this source from given view.
        """

        self.views_lock.acquire()

        if id(view) in self.views:
            del self.views[id(view)]
        stop_updater = not self.is_attached()

        self.views_lock.release()

        if stop_updater:
            self.stop_updater()

    def get_filename(self):
        return os.path.basename(self.filepath)

    def get_filepath(self):
        return self.filepath

    def is_attached(self):
        """
        Return ``True``, if this source is attached to at least one view.
        ``False`` otherwise.
        """
        return len(self.views) > 0

    def start_updater(self):
        """
        Start following physical source in separate update thread. This will
        be automatically called, as soon as this source is added to at least
        one source group.
        """

        if not self.updater:
            self.updater = TailSourceUpdater(self)
            self.updater.start()

    def stop_updater(self):
        """
        Stop following physical source by stopping update thread (if any).
        This will be automatically called after this source has been detached
        from all views.
        """

        if self.updater:
            # self.updater.signal.set('stop')
            self.updater.stop_signal.set()
            self.updater.join()
            self.updater = None


class TailSourceLine(object):

    """
    Class representing a single line from a source.

    :param source: Source, this line has been gathered from.
    :type source: ``TailSource``
    :param line: Actual line.
    :type line: ``String``
    """

    def __init__(self, source, line):
        self.line = line
        self.timestamp = time.time()
        self.source = source


class TailSourceUpdater(threading.Thread):

    """
    Class implementing actual tailing of a source within a separate thread.
    """

    def __init__(self, source):
        self.source = source
        # self.signal = signal.Signal()
        self.stop_signal = threading.Event()
        super(TailSourceUpdater, self).__init__()

    def run(self):
        """
        Start tailing source.
        """

        try:
            with open(self.source.filepath) as fh:
                # Seek to end of file and wait for new lines.
                fh.seek(0, 2)

                while True:
                    line = fh.readline()
                    if self.stop_signal.is_set():
                        break

                    if line:
                        self.source.add_line(TailSourceLine(self.source, line.rstrip('\r\n')))
                    else:
                        # self.signal.wait(0.2)
                        self.stop_signal.wait(0.2)
        except:
            print('Unexpected error in TailSourceUpdateThread for file "%s": %s' %
                  (self.source.filepath, sys.exc_info()[0]))
            raise

        # plugin.log(plugin.LOG_TRACE, 'Stopping tailing thread for file "%s"' % (self.source.filepath))
