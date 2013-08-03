# -*- coding: utf-8 -*-

try:
    from .packages.tail.commands import *                      # Python 3
    from .packages.tail.view import TailViewCloseListener
except (ValueError):
    from packages.tail.commands import *                       # Python 2
    from packages.tail.view import TailViewCloseListener
