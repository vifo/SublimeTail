# Tail for Sublime Text

[![Build Status](https://secure.travis-ci.org/vifo/SublimeTail.png)](http://travis-ci.org/vifo/SublimeTail)

[Tail](http://goo.gl/Pvbmrz) files in [Sublime Text 2](http://www.sublimetext.com/2) and [Sublime Text 3](http://www.sublimetext.com/3).

**Attention**: This plugin is considered to be alpha quality and currently under development. Documentation might not be up-to-date, as well as functionality missing or things simply not working as intended or expected. Also for now, you'll have to install this plugin manually via git or from ZIP. You have been warned.

#### Table of contents

* [Quick start](#quick-start)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
	+ [Key bindings](#configuration-key-bindings)
* [Troubleshooting](#troubleshooting)
	+ [Reporting bugs](#troubleshooting-reporting-bugs)
* [Say thanks](#say-thanks)
* [References / Links](#references-links)
* [Changes](#changes)

<a name="quick-start" />

## Quick start

* Install plugin in Sublime Text via Package Control, git or from ZIP
* Bring up the Command Palette (`Control+Shift+P` or `Command+Shift+P`), start typing "Tail" and choose action

Read on for detailed installation, usage, configuration and customization instructions.

<a name="installation" />

## Installation

* **With Package Control:** The easiest way to install *Tail* is through [Sublime Package Control](http://wbond.net/sublime_packages/package_control). If you're not using it yet, get it. Seriously.

  Once you have installed Package Control, restart Sublime Text and bring up the Command Palette (press `Control+Shift+P` on Linux/Windows, `Command+Shift+P` on OS X, or select `Tools->Command Palette...` from menu). Select *Package Control: Install Package*, wait till latest package list has been fetched, then select *Tail* from the list of available packages.

* **With Git:** Clone the repository in your Sublime Text *Packages* directory. Please note that the destination directory must be `Tail`.

        git clone -b devel https://github.com/vifo/SublimeTail Tail

The advantage of using either Package Control or git is, that the plugin will be automatically kept up-to-date.

* **From ZIP:** Download the latest version [as a ZIP archive](https://github.com/vifo/SublimeTail/archive/devel.zip) and copy the directory `SublimeTail-devel` from the archive to your Sublime Text *Packages* directory. Rename directory `SublimeTail-devel` to `Tail`.

The *Packages* directory locations are listed below. If using Sublime Text 2, be sure to replace `3` with `2` in directory names below.  Alternatively, selecting `Preferences->Browse Packages...` from Sublime Text menu will get you to the *Packages* directory also.

| OS            | Packages location                                         |
| ------------- | --------------------------------------------------------- |
| OS X          | `~/Library/Application Support/Sublime Text 3/Packages/`  |
| Linux         | `~/.config/sublime-text-3/Packages/`                      |
| Windows       | `%APPDATA%\Sublime Text 3\Packages\`                      |

<a name="usage" />

## Usage

After installation, open a file of your choice and open Command Palette. Start typing "Tail", choose desired action and hit return.

<a name="configuration" />

## Configuration

Until a detailed explanation of all possible configuration options is available, please check comments in the default settings (select `Preferences->Package Settings->Tail->Settings - Default`)

<a name="configuration-key-bindings" />

### Key bindings

None by default.

<a name="troubleshooting" />

## Troubleshooting

During normal operation, *Tail* will emit warnings and errors to the Sublime Text console (open with ``Control+` `` or select `View->Show Console` from menu). In order to enable additional diagnostic messages, adjust user setting "log_level" as follows:

| Level                     | Description                                                    |
| ------------------------- | -------------------------------------------------------------- |
| `0`, `error`              | Errors.                                                        |
| `1`, `warn`, `warning`    | Warnings.                                                      |
| `2`, `notice`             | Notices. This is the default logging level.                    |
| `3`, `info`               | Informational messages.                                        |
| `4`, `debug`              | Debugging messages.                                            |
| `5`, `trace`              | Tracing. Using this level might noticeably slow down plugin.   |

<a name="reporting-bugs" />

## Reporting bugs

In order to make bug hunting easier, please ensure, that you always run the *latest* version of *Tail*. Apart from this, please ensure, that you've set *Tail* log level to maximum (`"log_level": "trace"` in user settings), in order to get all debugging information possible. Also please include the following information, when submitting an issue:

* Operating system name (i.e. "Windows XP SP3", **not** "Windows")

* Operating system architecture (i.e. 32-bit, 64-bit)

* Sublime Text build number (open `Help->About`)

* Output from Sublime Text console

To gather this information quickly, open ST console, type in the following Python code as-is (in one line) and include its output in your issue:

```python
from __future__ import print_function, unicode_literals;import platform, sublime, datetime;print('-' * 78);print('Date/time: {0}'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')));print('Sublime Text version: {0}'.format(sublime.version()));print('Platform: {0}'.format(sublime.platform()));print('CPU architecture: {0}'.format(sublime.arch()));print('OS info: {0}'.format(repr(platform.platform())));print('-' * 78)
```

<a name="say-thanks" />

## Say thanks

I spend a lot of my scarce free time creating free software, and would appreciate any support you'd care to offer. If you'd like to thank me for the work I've done on this plugin, please consider:

* making a donation to me via [PayPal](https://www.paypal.com/) (log into PayPal and send donations to `vifo@cpan.org`)
* [star](https://github.com/blog/1204-notifications-stars) this plugin on GitHub
* twitter, blog or in general spread the word.

Please note that you don't *have* to do *any of the above* in order for me to continue to work on this plugin. I will continue to do so, for as long as it interests me and inasmuch I have free time to spend. Similarly, a donation made in this way probably won't make me work on this plugin harder, unless I get so many donations that I can consider working on free software full time (which seems unlikely at best).

Thank You.

<a name="changes" />

## References / Links

* [BareTail for Windows](http://www.baremetalsoft.com/baretail/)
* [GNU tail](https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html)
* [Native Windows tail from UnxUtils (as well as other common GNU utilities)](http://unxutils.sourceforge.net/)
* [tail on Wikipedia](http://goo.gl/Pvbmrz)

## Changes

Only latest changes are listed here. Refer to [full change log](https://github.com/vifo/SublimeTail/blob/devel/CHANGES.markdown) for all changes.

None yet. Plugin not released.
