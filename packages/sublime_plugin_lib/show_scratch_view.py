# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime_plugin
from . import compat


class SublimePluginLibShowScratchViewCommand(sublime_plugin.TextCommand):

    """
    Sublime Text command ``sublime_plugin_lib_show_scratch_view``. Opens a new
    scratch view with given contents.
    """

    def run(self, edit, contents=None, **kwargs):
        view = self.view
        options = {
            'spell_check': False,
            'scratch': True,
            'syntax': 'text',
        }

        # Validate options.
        for k in ['header', 'name', 'syntax']:
            if k in kwargs:
                if not isinstance(kwargs[k], compat.string_types):
                    raise ValueError('Option "%s" passed to run() must be a string' % (k))
                options[k] = kwargs[k]

        for k in ['spell_check', 'scratch']:
            if k in kwargs:
                if not isinstance(kwargs[k], bool):
                    raise ValueError('Option "%s" passed to run() must be a boolean' % (k))
                options[k] = kwargs[k]

        # Adjust view.
        if 'name' in options:
            view.set_name(options['name'])

        view.set_scratch(options['scratch'])
        view.settings().set('spell_check', options['spell_check'])

        if options['syntax'] == 'html':
            view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        elif options['syntax'] == 'text':
            view.set_syntax_file('Packages/Text/Plain text.tmLanguage')

        final_contents = ''
        if 'header' in options:
            final_contents = options['header'] + "\n"
            final_contents += len(options['header']) * "=" + "\n"
        if contents is not None:
            final_contents += contents

        view.insert(edit, view.size(), final_contents)


def show_scratch_view(view, contents=None, **kwargs):
    """
    Create new scratch view and display output.
    """

    kwargs['contents'] = contents
    output_view = view.window().new_file()
    output_view.run_command('sublime_plugin_lib_show_scratch_view', kwargs)
