from collections.abc import Iterable, Mapping
from typing import (
    Any,
    Callable,
    Optional,
    Protocol,
    TypeVar,
    Union,
    cast,
)

import pluggy

from typing_extensions import (
    TypeAlias,
)


class Format(Protocol):
    name: str
    suffixes: Optional[Iterable[str]]
    option_names: Optional[Iterable[str]]

    def __init__(self, options: Optional[Iterable[str]]) -> None: ...  # pragma: no cover

    def parse(self, data_string: str) -> Mapping[str, Any]: ...  # pragma: no cover


class FormatOptionUnknownError(Exception):
    def __init__(self, fmt: Union[type[Format], Format], option: str):
        self.fmt = fmt
        self.option = option

    def __str__(self) -> str:
        if self.fmt.option_names:
            return (
                f"Format {self.fmt.name}: option '{self.option}' is not valid; valid"
                f" options are '{', '.join(self.fmt.option_names)}'"
            )

        return (
            f"Format {self.fmt.name}: option '{self.option}' is not valid; this format"
            " does not accept any options."
        )


class FormatOptionUnsupportedError(Exception):
    def __init__(self, fmt: Union[type[Format], Format], option: str, message: str):
        self.fmt = fmt
        self.option = option
        self.message = message

    def __str__(self) -> str:
        return f"Format {self.fmt.name}: option '{self.option}' {self.message}."


class FormatOptionValueError(Exception):
    def __init__(self, fmt: Union[type[Format], Format], option: str, value: str, message: str):
        self.fmt = fmt
        self.option = option
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return (
            f"Format {self.fmt.name}: option '{self.option}' value '{self.value}'"
            f" {self.message}."
        )


F = TypeVar("F", bound=Callable[..., Any])
hookspec = cast(Callable[[F], F], pluggy.HookspecMarker("jinjanator"))

Identity: TypeAlias = str
Formats: TypeAlias = Mapping[str, type[Format]]
Filters: TypeAlias = Mapping[str, Callable[..., Any]]
Globals: TypeAlias = Mapping[str, Callable[..., Any]]
Tests: TypeAlias = Mapping[str, Callable[..., Any]]
Extensions: TypeAlias = Iterable[str]

PluginIdentityHook: TypeAlias = Callable[[], Identity]
PluginFormatsHook: TypeAlias = Callable[[], Formats]
PluginFiltersHook: TypeAlias = Callable[[], Filters]
PluginTestsHook: TypeAlias = Callable[[], Tests]
PluginGlobalsHook: TypeAlias = Callable[[], Globals]
PluginExtensionsHook: TypeAlias = Callable[[], Extensions]

plugin_identity_hook = cast(
    Callable[[PluginIdentityHook], PluginIdentityHook],
    pluggy.HookimplMarker("jinjanator"),
)
plugin_formats_hook = cast(
    Callable[[PluginFormatsHook], PluginFormatsHook],
    pluggy.HookimplMarker("jinjanator"),
)
plugin_filters_hook = cast(
    Callable[[PluginFiltersHook], PluginFiltersHook],
    pluggy.HookimplMarker("jinjanator"),
)
plugin_tests_hook = cast(
    Callable[[PluginTestsHook], PluginTestsHook],
    pluggy.HookimplMarker("jinjanator"),
)
plugin_globals_hook = cast(
    Callable[[PluginGlobalsHook], PluginGlobalsHook],
    pluggy.HookimplMarker("jinjanator"),
)
plugin_extensions_hook = cast(
    Callable[[PluginExtensionsHook], PluginExtensionsHook],
    pluggy.HookimplMarker("jinjanator"),
)


class PluginHooks(Protocol):
    @staticmethod
    @hookspec
    def plugin_identities() -> Identity:
        """Returns identity as string"""

    @staticmethod
    @hookspec
    def plugin_formats() -> Formats:
        """Returns dict of formats"""

    @staticmethod
    @hookspec
    def plugin_filters() -> Filters:
        """Returns dict of filter functions"""

    @staticmethod
    @hookspec
    def plugin_globals() -> Globals:
        """Returns dict of global functions"""

    @staticmethod
    @hookspec
    def plugin_tests() -> Tests:
        """Returns dict of test functions"""

    @staticmethod
    @hookspec
    def plugin_extensions() -> Extensions:
        """Returns list of extensions to add to Jinja2"""


class PluginHookCallers(Protocol):
    @staticmethod
    def plugin_identities() -> Iterable[Identity]:
        """Returns iterable of strings of identities"""

    @staticmethod
    def plugin_formats() -> Iterable[Formats]:
        """Returns iterable of dicts of formats"""

    @staticmethod
    def plugin_filters() -> Iterable[Filters]:
        """Returns iterable of dicts of filter functions"""

    @staticmethod
    def plugin_globals() -> Iterable[Globals]:
        """Returns iterable of dicts of global functions"""

    @staticmethod
    def plugin_tests() -> Iterable[Tests]:
        """Returns iterable of dicts of test functions"""

    @staticmethod
    def plugin_extensions() -> Iterable[Extensions]:
        """Returns iterable of list of extensions to add to Jinja2"""
