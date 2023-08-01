from __future__ import annotations

import jinjanator_plugin_example as plugin  # type: ignore[import]
import pytest

from jinjanator_plugins import (
    FormatOptionUnknownError,
    FormatOptionUnsupportedError,
    FormatOptionValueError,
)


def test_filter() -> None:
    assert "Oneg" == plugin.rot13_filter("Bart")


def test_test() -> None:
    assert True is plugin.is_len12_test("Bartholomew1")
    assert False is plugin.is_len12_test("Bart")


def test_format() -> None:
    result = plugin.SpamFormat.parser("", [])
    assert "cheese" in result
    assert "spam and cheese" == result["cheese"]


def test_format_option() -> None:
    result = plugin.SpamFormat.parser("", ["ham"])
    assert "cheese" in result
    assert "ham and cheese" == result["cheese"]


def test_format_option_unknown() -> None:
    with pytest.raises(FormatOptionUnknownError):
        plugin.SpamFormat.parser("", ["unk"])


def test_format_option_unsupported() -> None:
    with pytest.raises(FormatOptionUnsupportedError):
        plugin.SpamFormat.parser("", ["uns"])


def test_format_option_value() -> None:
    with pytest.raises(FormatOptionValueError):
        plugin.SpamFormat.parser("", ["val"])
