from __future__ import annotations

from typing import cast

import jinjanator_plugin_example as plugin
import pluggy  # type: ignore[import]
import pytest

from jinjanator_plugins import (
    PluginHookCallers,
    PluginHooks,
)


@pytest.fixture(scope="module")
def hook_callers() -> PluginHookCallers:
    pm = pluggy.PluginManager("jinjanator")
    pm.add_hookspecs(PluginHooks)
    pm.register(plugin)
    return cast(PluginHookCallers, pm.hook)


def test_identity(hook_callers) -> None:
    result = hook_callers.plugin_identities()
    assert len(result) == 1
    assert "example" == result[0]


def test_filter(hook_callers) -> None:
    result = hook_callers.plugin_filters()
    assert len(result) == 1
    assert "rot13" in result[0]
    assert plugin.rot13_filter == result[0]["rot13"]


def test_test(hook_callers) -> None:
    result = hook_callers.plugin_tests()
    assert len(result) == 1
    assert "len12" in result[0]
    assert plugin.is_len12_test == result[0]["len12"]


def test_format(hook_callers) -> None:
    result = hook_callers.plugin_formats()
    assert len(result) == 1
    assert "spam" in result[0]
    assert plugin.spam_format == result[0]["spam"].parser
    assert len(result[0]["spam"].suffixes) == 1
    assert ".spam" == result[0]["spam"].suffixes[0]
