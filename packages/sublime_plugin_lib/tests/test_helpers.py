# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import pytest
import sys
import os

from ..mock import sublime
from .. import helpers
from ..helpers import *


@pytest.fixture()
def clean_env():
    if 'SUBLIME_PLUGIN_LIB_TEST_FOOBAR' in os.environ:
        del os.environ['SUBLIME_PLUGIN_LIB_TEST_FOOBAR']


set_env_flag(prefix='SUBLIME_PLUGIN_LIB_TEST', flag='FOOBAR', value=True)


def test_get_default_subprocess_args():
    result = get_default_subprocess_args()
    assert isinstance(result, dict)


def test_get_env_flag(clean_env):
    assert get_env_flag('nonexistant') is False

    os.environ['SUBLIME_PLUGIN_LIB_TEST_FOOBARBAZ'] = "1"
    assert get_env_flag('foobarbaz', prefix='sublime_plugin_lib_test') is True

    os.environ['SUBLIME_PLUGIN_LIB_TEST_FOOBARBAZ'] = "0"
    assert get_env_flag('foobarbaz') is False

    if 'SUBLIME_PLUGIN_LIB_TEST_FOOBARBAZ' in os.environ:
        del os.environ['SUBLIME_PLUGIN_LIB_TEST_FOOBARBAZ']
    assert get_env_flag('foobarbaz') is False


def test_is_ascii_safe_string():
    assert is_ascii_safe_string(input='foobarbaz') is True
    assert is_ascii_safe_string(input='äöü') is False


def test_pp():
    assert pp(None) == '<None>'
    assert pp('Hello world') == '"Hello world"'
    assert pp(['Hello', 'world']) == '"Hello" "world"'


def test_restore_env():
    result = restore_env({})
    assert isinstance(result, bool)


def test_save_and_prepare_env():
    result = save_and_prepare_env()
    assert isinstance(result, dict)


def test_set_env_flag():
    result = set_env_flag(flag='foobar', prefix='sublime_plugin_lib_test', value=True)
    assert result is None
    assert os.environ['SUBLIME_PLUGIN_LIB_TEST_FOOBAR'] == '1'

    result = set_env_flag(flag='foobar', prefix='sublime_plugin_lib_test', value="BAZ")
    assert os.environ['SUBLIME_PLUGIN_LIB_TEST_FOOBAR'] == "BAZ"
    assert result == "1"

    result = set_env_flag(flag='foobar', prefix='sublime_plugin_lib_test', value=None)
    assert not 'SUBLIME_PLUGIN_LIB_TEST_FOOBAR' in os.environ
    assert result == "BAZ"
