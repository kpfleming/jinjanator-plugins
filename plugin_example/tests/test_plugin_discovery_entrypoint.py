from typing import cast

import pluggy
import pytest

from jinjanator_plugins import (
    PluginHookCallers,
    PluginHooks,
)


@pytest.fixture(scope="module")
def hook_callers() -> PluginHookCallers:
    pm = pluggy.PluginManager("jinjanator")
    pm.add_hookspecs(PluginHooks)
    pm.load_setuptools_entrypoints("jinjanator")
    return cast(PluginHookCallers, pm.hook)


def test_identity(hook_callers: PluginHookCallers) -> None:
    result = iter(hook_callers.plugin_identities())

    _identity = next(result)
    with pytest.raises(StopIteration):
        next(result)

    assert "example" == _identity


def test_filter(hook_callers: PluginHookCallers) -> None:
    result = iter(hook_callers.plugin_filters())

    filters = next(result)
    with pytest.raises(StopIteration):
        next(result)

    assert "rot13" in filters
    assert 1 == len(filters.keys())


def test_test(hook_callers: PluginHookCallers) -> None:
    result = iter(hook_callers.plugin_tests())

    tests = next(result)
    with pytest.raises(StopIteration):
        next(result)

    assert "len12" in tests
    assert 1 == len(tests.keys())


def test_format(hook_callers: PluginHookCallers) -> None:
    result = iter(hook_callers.plugin_formats())

    fmts = next(result)
    with pytest.raises(StopIteration):
        next(result)

    assert "spam" in fmts
    _fmt = fmts["spam"]

    assert _fmt.suffixes is not None
    suffixes = iter(_fmt.suffixes)
    _suffix = next(suffixes)
    with pytest.raises(StopIteration):
        next(suffixes)

    assert ".spam" == _suffix

    assert _fmt.option_names is not None
    option_names = iter(_fmt.option_names)
    _option = next(option_names)
    with pytest.raises(StopIteration):
        next(option_names)

    assert "ham" == _option
