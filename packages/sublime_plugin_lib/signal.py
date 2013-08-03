# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import threading


class Signal:

    """
    Signal class for inter-thread synchronization. Similar to
    ``threading.Event``, but allows for setting additional flags, which can be
    queried by the receiver of the signal.
    """

    def __init__(self):
        self._flags = {}
        self._cond = threading.Condition(threading.Lock())
        self._is_signaled = False

    def clear(self, flag=None):
        """
        Sets state to *not signaled* and clears all flags. If a specific flag is
        given in ``flag``, clears this flag only and adjust state (will be still
        *signaled*, if any set flags remain).

        :returns:
            Nothing.
        """

        if flag is None:
            self._is_signaled = False
            self._flags = {}
        else:
            self._cond.acquire()
            try:
                if flag in self._flags:
                    del self._flags[flag]
                    self._is_signaled = len(self._flags) > 0
            finally:
                self._cond.release()

    def is_set(self, flag=None, clear=False):
        """
        Returns signal state.

        :param flag:
            If a flag is passed, ``True`` will be returned only, if this flag is
            set.
        :type flag:
            *str*
        :param clear:
            If ``clear`` is set to ``True``, will clear this flag, before
            returning.
        :type clear:
            *bool*
        :returns:
            ``True`` if signaled, ``False`` otherwise
        :rtype:
            bool
        """

        self._cond.acquire()
        try:
            if not self._is_signaled:
                # Not signaled. Nothing to do, return False immediately.
                return False
            else:
                if flag is None:
                    # Signaled and not querying specific flag. Optionally
                    # clear and return True.
                    if clear:
                        self._is_signaled = False
                        self._flags = {}
                    return True

                if flag in self._flags:
                    # Flag is set. Optionally clear, set new signaled state
                    # and return True.
                    if clear:
                        del self._flags[flag]
                        self._is_signaled = len(self._flags) > 0
                    return True

                # Queried flag not set.
                return False
        finally:
            self._cond.release()

    def set(self, *flags):
        """
        Sets state to *signaled* and sets all flags passed in ``flags`` (if
        any). If the previous state was *not signaled*, sends a notification
        to all threads waiting for this signal. Otherwise updates flags
        without sending notifications.

        :returns:
            Nothing.
        """

        self._cond.acquire()
        try:
            for flag in flags:
                self._flags[flag] = True

            # Notify all threads waiting for this signal, but only, if state
            # was not signaled before.
            if not self._is_signaled:
                self._is_signaled = True
                self._cond.notify_all()

        finally:
            self._cond.release()

    def wait(self, timeout=None, clear=False):
        """
        Wait for signal to become *signaled*.

        :param timeout:
            Optional timeout.
        :type timeout:
            ``float``
        :param clear:
            If set to ``True``, state will be reset to *not signaled* upon
            return.
        :type clear:
            ``bool``
        :returns:
            - ``False`` on timeout
            - ``True`` if signal is set, but flag list is empty
            - ``list`` with set flags otherwise
        """

        self._cond.acquire()
        try:
            is_signaled = self._is_signaled
            if not is_signaled:
                self._cond.wait(timeout)
                is_signaled = self._is_signaled

            if not is_signaled:
                return False
            if not len(self._flags):
                return True
            return self._flags.keys()
        finally:
            self._cond.release()
