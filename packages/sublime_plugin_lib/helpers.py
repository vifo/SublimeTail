# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import os
import subprocess
import sys

from . import compat

"""
Miscellaneous helpers for `Sublime Text` plugins.

:synopsis: Miscellaneous helpers for `Sublime Text` plugins.
:moduleauthor: Victor Foitzik <vifo@cpan.org>
"""

#: :synopsis: Miscellaneous plugin helpers


__all__ = [
    'get_default_subprocess_args',
    'get_env_flag',
    'is_ascii_safe_string',
    'pp',
    'restore_env',
    'save_and_prepare_env',
    'set_env_flag',
]


def get_default_subprocess_args():
    # Prepare arguments for subprocess call.
    subprocess_args = {
        'bufsize': -1,
        'shell': False,
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
    }

    # Hide console window on Windows.
    if sys.platform.startswith('win'):
        subprocess_args['startupinfo'] = subprocess.STARTUPINFO()
        subprocess_args['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW

    return subprocess_args


def is_ascii_safe_string(input):
    """
    Returns ``True``, if string passed in ``input`` can be safely encoded in
    ASCII, ``False`` otherwise.
    """

    input_bytes = input.encode('utf-8')

    try:
        input_bytes.decode('ascii')
        return True
    except (UnicodeDecodeError, UnicodeEncodeError):
        return False


def pp(string):
    """
    Return a pretty printed representation of string for debugging/logging
    purposes.
    """

    if string is None:
        return '<None>'

    tokens = []
    if isinstance(string, compat.list_types):
        for i in string:
            tokens.append('"{0}"'.format(i))
    else:
        tokens.append('"{0}"'.format(string))

    return ' '.join(tokens)


def restore_env(orig_env={}):
    if sys.platform.startswith('win'):

        # Restore environment variables.
        if 'CYGWIN' in orig_env:
            os.environ['CYGWIN'] = orig_env['CYGWIN']
        elif 'CYGWIN' in os.environ:
            del os.environ['CYGWIN']

        if 'LANG' in orig_env:
            os.environ['LANG'] = orig_env['LANG']
        elif 'LANG' in os.environ:
            del os.environ['LANG']

    return True


def save_and_prepare_env():
    orig_env = {}

    # On Windows, ensure, that we have CYGWIN environment variables set, even
    # if we don't known, whether we actually are using Cygwin.
    if sys.platform.startswith('win'):
        if 'CYGWIN' in os.environ and not re.match(r'\bnodosfilewarning\b', os.environ['CYGWIN']):
            orig_env['CYGWIN'] = os.environ['CYGWIN']
            os.environ['CYGWIN'] += ' nodosfilewarning'
        else:
            os.environ['CYGWIN'] = 'nodosfilewarning'

        if 'LANG' in os.environ:
            orig_env['LANG'] = os.environ['LANG']

        os.environ['LANG'] = 'C'

    return orig_env


def get_env_flag(flag, prefix=''):
    """
    Returns, whether given flag is set in environment. The name of the flag
    passed in ``flag`` will be prefixed with ``prefix_`` (if not blank) and
    uppercased. Returns ``True`` if resulting flag is set (i.e. ``1``)
    ``False`` otherwise.

    >>> import os
    >>> os.environ["MY_AWESOME_APP_LOG_LEVEL"] = "2"
    >>> get_env_flag("log_level", prefix="my_awesome_app")
    '2'
    """
    key = flag.upper()
    if prefix != '':
        key = prefix.upper() + '_' + key

    if key in os.environ:
        if os.environ[key] == "0":
            return False
        elif os.environ[key] == "1":
            return True
        else:
            return os.environ[key]
    else:
        return False


def set_env_flag(flag, prefix='', value=True):
    """
    Set given flag in environment. The name of the flag passed in ``flag``
    will be prefixed with ``prefix_``, if given, and uppercased. Sets
    environment variable to appropriate ``value``. Boolean values will be
    stored as ``0`` and ``1`` for ``False`` and ``True`` respectively.

    Returns previous value or ``None`` if environment variable was unset
    before.
    """

    key = flag.upper()
    if prefix != '':
        key = (prefix + '_').upper() + key

    previous = None
    if key in os.environ:
        previous = os.environ[key]

    if value is None:
        if key in os.environ:
            del os.environ[key]
    else:
        if isinstance(value, bool):
            os.environ[key] = "1" if value else "0"
        else:
            os.environ[key] = value

    return previous
