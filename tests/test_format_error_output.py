from collections.abc import Iterable, Mapping
from typing import Optional

from jinjanator_plugins import (
    FormatOptionUnknownError,
    FormatOptionUnsupportedError,
    FormatOptionValueError,
)


class FormatNoOptions:
    name = "test"
    suffixes: Optional[Iterable[str]] = ()
    option_names: Optional[Iterable[str]] = ()

    def __init__(self, options: Optional[Iterable[str]]) -> None:
        pass

    def parse(
        self,
        data_string: str,  # noqa: ARG002
    ) -> Mapping[str, str]:
        return {}


class FormatOptions:
    name = "test"
    suffixes: Optional[Iterable[str]] = ()
    option_names: Optional[Iterable[str]] = ("bart",)

    def __init__(self, options: Optional[Iterable[str]]) -> None:
        pass

    def parse(
        self,
        data_string: str,  # noqa: ARG002
    ) -> Mapping[str, str]:
        return {}


def test_unknown_no_options() -> None:
    result = str(FormatOptionUnknownError(FormatNoOptions, "midge"))
    assert "test:" in result
    assert "'midge'" in result
    assert "accept any options" in result


def test_unknown_options() -> None:
    result = str(FormatOptionUnknownError(FormatOptions, "midge"))
    assert "test:" in result
    assert "'midge'" in result
    assert "'bart'" in result


def test_unsupported() -> None:
    result = str(FormatOptionUnsupportedError(FormatOptions, "midge", "not supported"))
    assert "test:" in result
    assert "'midge'" in result
    assert "not supported" in result


def test_value() -> None:
    result = str(FormatOptionValueError(FormatOptions, "midge", "milhouse", "not valid"))
    assert "test:" in result
    assert "'midge'" in result
    assert "'milhouse'" in result
    assert "not valid" in result
