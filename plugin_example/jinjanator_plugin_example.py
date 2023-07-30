from __future__ import annotations

import codecs

from typing import Mapping

from jinjanator_plugins import (
    Filters,
    Format,
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


def spam_format(
    data_string: str,  # noqa: ARG001
    options: list[str] | None = None,
) -> Mapping[str, str]:
    ham = False

    if options:
        for option in options:
            if option == "ham":
                ham = True
            elif option == "uns":
                msg = f"Format option {option} is not supported."
                raise FormatOptionUnsupportedError(msg)
            elif option == "val":
                msg = f"Format option {option} has an invalid value."
                raise FormatOptionValueError(msg)
            else:
                msg = f"Format option {option} is not known"
                raise FormatOptionUnknownError(msg)

    if ham:
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
    return {"spam": Format(parser=spam_format, suffixes=[".spam"])}
