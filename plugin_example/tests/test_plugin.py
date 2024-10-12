import jinjanator_plugin_example as plugin  # type: ignore[import-not-found]
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
    result = plugin.SpamFormat([]).parse("")
    assert "cheese" in result
    assert "spam and cheese" == result["cheese"]


def test_format_option() -> None:
    result = plugin.SpamFormat(["ham"]).parse("")
    assert "cheese" in result
    assert "ham and cheese" == result["cheese"]


def test_format_option_unknown() -> None:
    with pytest.raises(FormatOptionUnknownError):
        plugin.SpamFormat(["unk"])


def test_format_option_unsupported() -> None:
    with pytest.raises(FormatOptionUnsupportedError):
        plugin.SpamFormat(["uns"])


def test_format_option_value() -> None:
    with pytest.raises(FormatOptionValueError):
        plugin.SpamFormat(["val"])
