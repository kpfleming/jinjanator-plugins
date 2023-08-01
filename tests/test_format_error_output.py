from __future__ import annotations

from typing import Any, Mapping

from jinjanator_plugins import (
    Format,
    FormatOptionUnknownError,
    FormatOptionUnsupportedError,
    FormatOptionValueError,
)


def fake_format_parser(
    data_string: str, options: list[str] | None  # noqa: ARG001
) -> Mapping[str, Any]:
    return {}


test_format_no_options = Format(
    name="test", parser=fake_format_parser, suffixes=[], options=[]
)
test_format_options = Format(
    name="test", parser=fake_format_parser, suffixes=[], options=["bart"]
)


def test_unknown_no_options() -> None:
    result = str(FormatOptionUnknownError(test_format_no_options, "midge"))
    assert "test:" in result
    assert "'midge'" in result
    assert "accept any options" in result


def test_unknown_options() -> None:
    result = str(FormatOptionUnknownError(test_format_options, "midge"))
    assert "test:" in result
    assert "'midge'" in result
    assert "'bart'" in result


def test_unsupported() -> None:
    result = str(
        FormatOptionUnsupportedError(test_format_options, "midge", "not supported")
    )
    assert "test:" in result
    assert "'midge'" in result
    assert "not supported" in result


def test_value() -> None:
    result = str(
        FormatOptionValueError(test_format_options, "midge", "milhouse", "not valid")
    )
    assert "test:" in result
    assert "'midge'" in result
    assert "'milhouse'" in result
    assert "not valid" in result
