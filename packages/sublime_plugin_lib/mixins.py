# -*- coding: utf-8 -*-

"""
Dynamically mix additional methods into a sublime.View instance to provide
additional functionality.
"""

from __future__ import print_function, unicode_literals
import sublime
import types

from . import compat

__all__ = [
    'enhance_sublime_view',
]


def enhance_sublime_view(view):
    """
    Mix additional methods into sublime.View instance.
    """

    def append(self, edit, contents):
        """
        Append contents to end of buffer.
        """

        self.insert(edit, self.size(), "\n".join(contents) if isinstance(contents, compat.list_types) else contents)

    def replace_contents(self, edit, region, contents, method='default'):
        """
        Replace view contents using specified method.
        """

        if method == 'default':
            print("using method default")
            self.replace(edit, region, contents)

        elif method == 'incremental':
            print("using method incremental")
            lines_left = contents.split("\n")
            regions_left = self.split_by_newlines(region)

            while lines_left and regions_left:
                cur_region = regions_left.pop(0)
                new_line = lines_left.pop(0)

                if self.substr(cur_region) != new_line:
                    self.replace(edit, cur_region, new_line)
                    regions_left = self.split_by_newlines(sublime.Region(cur_region.begin(), self.size()))
                    regions_left.pop(0)

            # Erase rest of regions
            if regions_left:
                self.erase(edit, sublime.Region(regions_left[0].begin(), self.size()))

            # Add rest of lines
            if lines_left:
                self.append(edit, lines_left)

            # Remove trailing newlines (keep one at end of buffer)
            self.remove_trailing_newlines(edit)

        else:
            raise ValueError('Argument "method" passed to replace_contents() must be either "default" or "incremental"')

    def remove_trailing_newlines(self, edit, region=None, keep_last_newline=True):
        """
        Remove trailing newlines from buffer.
        """

        while self.size() >= 2:
            if self.substr(sublime.Region(self.size() - 2, self.size())) == "\n\n":
                self.erase(edit, sublime.Region(self.size() - 1, self.size()))
            else:
                break

    def sel_non_empty(self):
        """
        Return list of sublime.Region objects containing all non-empty selections.

        Note that since we cannot instantiate a sublime.RegionSet object, this
        method will return a list containing regions, whereas the default .sel()
        method returns a sublime.RegionSet.
        """

        selections = []
        for region in self.sel():
            if not region.empty():
                selections.append(region)

        return selections

    def whole_buffer_region(self):
        """
        Return region representing whole buffer.
        """

        return sublime.Region(0, self.size())

    # Mix methods into passed view.
    if not hasattr(view, '__sublime_plugin_lib_mixed_in'):
        view.append = types.MethodType(append, view)
        view.remove_trailing_newlines = types.MethodType(remove_trailing_newlines, view)
        view.replace_contents = types.MethodType(replace_contents, view)
        view.sel_non_empty = types.MethodType(sel_non_empty, view)
        view.whole_buffer_region = types.MethodType(whole_buffer_region, view)

    return view
