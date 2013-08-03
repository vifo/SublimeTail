# -*- coding: utf-8 -*-

"""
Access plugin settings and provide simple logging facility.
"""

import sublime
from ..sublime_plugin_lib import compat

NAME = "Tail"
VERSION = "0.1.0"
GUI_NAME = "Tail"

LOG_LEVELS = {
    'error': 0,
    'warning': 1,
    'warn': 1,
    'notice': 2,
    'info': 3,
    'debug': 4,
    'trace': 5,
}

LOG_ERROR = 0
LOG_WARNING = 1
LOG_NOTICE = 2
LOG_INFO = 3
LOG_DEBUG = 4
LOG_TRACE = 5


def get_log_level():
    """
    Returns current log level.

    :returns:
        Log level corresponding to one of defined ``LOG_*`` constants.
    :rtype:
        *int*
    """

    log_level = get_setting('log_level')
    if isinstance(log_level, compat.string_types):
        log_level = LOG_LEVELS[log_level]
    return log_level


def get_setting(name, default=None):
    """
    Returns a single setting loaded from ``*.sublime-settings``, optionally
    using a default value.

    :param name:
        Name of setting to retrieve, separated with dots, e.g.
        "renderers.cpan.enabled"
    :type name:
        *str*
    :param default:
        Default value which will be returned, if either final setting or any
        intermediate settings are None.
    :returns:
        Resulting value for given setting.
    """

    s = sublime.load_settings('%s.sublime-settings' % (NAME))
    keys = name.split('.')

    # First element handled via .get()
    s = s.get(keys.pop(0))
    while len(keys):
        key = keys.pop(0)
        if isinstance(s, dict) and key in s:
            s = s[key]
        else:
            s = default
            break

    return s


def is_enabled():
    """
    Returns ``True``, if plugin is enabled, ``False`` otherwise.

    :rtype:
        *bool*
    """

    return True if get_setting('enabled') else False


def log(level, *messages):
    """
    Logs given ``messages``, if current logging level is higher or equal
    ``level``.

    :param level:
        Log level. Must be either a ``LOG_*`` constant or a string.
    :param *messages:
        One or more messages to be logged.
    :returns:
        *Nothing*
    """

    # Map stringy level to numeric one.
    if isinstance(level, compat.string_types):
        level = LOG_LEVELS[level]

    if level <= get_log_level():
        print(NAME + ': ' + (' '.join(messages)))
