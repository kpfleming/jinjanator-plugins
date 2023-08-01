from __future__ import annotations

import codecs

from typing import Iterable, Mapping

from jinjanator_plugins import (
    Filters,
    FormatOptionUnknownError,
    FormatOptionUnsupportedError,
    FormatOptionValueError,
    Formats,
    Identity,
    Tests,
    plugin_filters_hook,
    plugin_formats_hook,
    plugin_identity_hook,
    plugin_tests_hook,
)


def rot13_filter(value: str) -> str:
    return codecs.encode(value, "rot13")


def is_len12_test(value: str) -> bool:
    return len(value) == 12  # noqa: PLR2004


class SpamFormat:
    name = "spam"
    suffixes: Iterable[str] | None = (".spam",)
    option_names: Iterable[str] | None = ("ham",)

    def __init__(self, options: Iterable[str] | None) -> None:
        self.ham = False

        if options:
            for option in options:
                if option == "ham":
                    self.ham = True
                elif option == "uns":
                    raise FormatOptionUnsupportedError(self, option, "is not supported")
                elif option == "val":
                    raise FormatOptionValueError(self, option, "", "is not valid")
                else:
                    raise FormatOptionUnknownError(self, option)

    def parse(
        self,
        data_string: str,  # noqa: ARG002
    ) -> Mapping[str, str]:
        if self.ham:
            return {
                "ham": "ham",
                "cheese": "ham and cheese",
                "potatoes": "ham and potatoes",
            }

        return {
            "spam": "spam",
            "cheese": "spam and cheese",
            "potatoes": "spam and potatoes",
        }


@plugin_identity_hook
def plugin_identities() -> Identity:
    return "example"


@plugin_filters_hook
def plugin_filters() -> Filters:
    return {"rot13": rot13_filter}


@plugin_tests_hook
def plugin_tests() -> Tests:
    return {"len12": is_len12_test}


@plugin_formats_hook
def plugin_formats() -> Formats:
    return {SpamFormat.name: SpamFormat}
