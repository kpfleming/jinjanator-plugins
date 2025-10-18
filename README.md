# jinjanator-plugins

<a href="https://opensource.org"><img height="150" align="left" src="https://opensource.org/files/OSIApprovedCropped.png" alt="Open Source Initiative Approved License logo"></a>
[![CI](https://github.com/kpfleming/jinjanator-plugins/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/kpfleming/jinjanator-plugins/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-31019/)
[![License - Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-9400d3.svg)](https://spdx.org/licenses/Apache-2.0.html)
[![Code Style - Black](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)
[![Types - Mypy](https://img.shields.io/badge/Types-Mypy-blue.svg)](https://github.com/python/mypy)
[![Code Quality - Ruff](https://img.shields.io/badge/Code%20Quality-Ruff-red.svg)](https://github.com/astral-sh/ruff)
[![Project Management - Hatch](https://img.shields.io/badge/Project%20Management-Hatch-purple.svg)](https://github.com/pypa/hatch)
[![Testing - Pytest](https://img.shields.io/badge/Testing-Pytest-orange.svg)](https://github.com/pytest-dev/pytest)

This repo contains `jinjanator-plugins`, a set of types and decorators
which can be used to implement plugins for the
[jinjanator](https://github.com/kpfleming/jinjanator) tool.

Open Source software: [Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html)

## &nbsp;
<!-- fancy-readme start -->

jinjanator can be extended through the use of plugins; these are
Python packages installed into the same environment as the tool
itself, which use special markers to 'hook' into various
features. There is a minimal example in the
[plugin_example](plugin_example) directory which demonstrates three of
the four possible hooks.

For a more complete example, intended for publication, check out the
[jinjanator-plugin-ansible](https://github.com/kpfleming/jinjanator-plugin-ansible)
repository.

Plugins can provide:

* *formats*: data parsers used to extract data from input files.

* *filters*: functions used in Jinja2 templates to transform data.

* *tests*: functions used in Jinja2 templates to make decisions in
  conditional logic.

* *globals*: functions used in Jinja2 templates to obtain data from
  external sources.

* *extensions*: Jinja2 extensions that can add extra filters, tests,
  globals or even extend the parser.

For more details on the functionality and requirements for 'filters',
'tests', 'globals', and 'extensions', refer to the Jinja2 documentation.

## Installation

Normally there is no need to install this package; instead it should
be listed as one of the dependencies for the plugin package itself.

Note: It is *strongly* recommended to pin the dependency for this
package to a specific version, or if not, a "year.release" version
range (like "23.2.*"). Failure to pin to a very narrow range of
versions may result in breakage of a plugin when the API is changed in
a non-backward-compatible fashion.

This is somewhat similar to *semantic versioning*, except not that :)

## Basic structure

A minimal plugin consists of two files:

* `pyproject.toml`: provides package and project information, and
  build instructions

* Python source: provides functions to implement the desired features,
  and hook markers to plug them into jinjanator

### pyproject.toml

```toml
[build-system]
build-backend = "setuptools.build_meta"
requires = [
  "setuptools>=61",
]

[project]
name = "jinjanator-plugin-example"
version = "0.0.0"
dependencies = [
  "jinjanator-plugins==23.3.0",
]

[tool.setuptools]
py-modules = ["jinjanator_plugin_example"]

[project.entry-points.jinjanator]
example = "jinjanator_plugin_example"
```

#### build-system

Any PEP517-compatible build system can be used, for this simple
example `setuptools` is being used.

#### project

The `name` and `version` are required to build a package containing
the plugin. Note the *specific version dependency* on the
`jinjanator-plugins` package.

#### tool.setuptools

This section tells `setuptools` to include a single source file (not a
package directory) into the distribution. Note that this is a *module
name*, not a *file name*, so there is no `.py` extension.

#### project.entry-points.jinjanator

This is the first part of the 'magic' mechanism which allows
jinjanator to find the plugin. The entry here (which can use any name,
but should be related to the project name in order to avoid conflicts)
creates an 'entry point' which jinjanator can use to find the plugin;
the value is the name of the module which jinjanator should import to
find the plugin's hooks (and must match the name specified in the
`tool.setuptools` section).

### jinjanator_plugin_example.py

```python
import codecs

from jinjanator_plugins import (
    FormatOptionUnknownError,
    FormatOptionUnsupportedError,
    FormatOptionValueError,
    plugin_filters_hook,
    plugin_formats_hook,
    plugin_identity_hook,
    plugin_tests_hook,
    plugin_extensions_hook,
)


def rot13_filter(value):
    return codecs.encode(value, "rot13")


def is_len12_test(value):
    return len(value) == 12


class SpamFormat:
    name = "spam"
    suffixes = (".spam",)
    option_names = ("ham",)

    def __init__(self, options):
        self.ham = False

        if options:
            for option in options:
                if option == "ham":
                    self.ham = True

    def parse(self, data_string):
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
def plugin_identities():
    return "example"


@plugin_filters_hook
def plugin_filters():
    return {"rot13": rot13_filter}


@plugin_tests_hook
def plugin_tests():
    return {"len12": is_len12_test}


@plugin_formats_hook
def plugin_formats():
    return {SpamFormat.name: SpamFormat}


@plugin_extensions_hook
def plugin_extensions():
    return ['jinja2.ext.debug']
```

Note that the real example makes use of type annotations, but they
have been removed here for simplicity.

#### Imports

The imports from `jinjanator_plugins` are necessary for the plugin to:
* Mark the hooks it wishes to use to provide additional features.
* Construct one (or more) `Format` objects to describe the formats it
  supports, if any.
* Raise option-related exceptions from its format function, if any.

#### rot13_filter

A simple filter function which applies the `rot13` transformation to
the string value it receives.

#### is_len12_test

A simple test function which returns `True` if the value it receives
has length 12.

#### SpamFormat

A class providing a simple format function which ignores the content
provided (which jinjanator would have read from a data file), and
instead returns one of two canned responses based on whether the `ham`
option has been provided by the user.

The `parse` method is the function which does the work; the `__init__`
method handles options provided by the user; the class attributes
provide details of the format.

#### plugin_identities

The hook function which will be called by jinjanator to allow this
plugin to identify itself; the `@plugin_identities_hook` decorator
marks the function so that it will be found.

The function must return a string, which can contain any information
needed to identify the plugin. This should include the plugin's name
and version, and can include versions of any packages on which it
depends.

This string will be included in the output generated by `jinjanate
--version`, so it should not include any newlines or other formatting
characters.

Note that the function *must* be named `plugin_identities`; it is the
second part of the 'magic' mechanism mentioned above.

#### plugin_filters

The hook function which will be called by jinjanator to allow this
plugin to register any filter functions it provides; the
`@plugin_filters_hook` decorator marks the function so that it will be
found.

The function must return a dictionary, with each key being a filter
function name (the name which will be used in the Jinja2 template to
invoke the function) and the corresponding value being a reference to
the function itself.

Note that the function *must* be named `plugin_filters`; it is the
second part of the 'magic' mechanism mentioned above.

#### plugin_tests

The hook function which will be called by jinjanator to allow this
plugin to register any test functions it provides; the
`@plugin_tests_hook` decorator marks the function so that it will be
found.

The function must return a dictionary, with each key being a test
function name (the name which will be used in the Jinja2 template to
invoke the function) and the corresponding value being a reference to
the function itself.

Note that the function *must* be named `plugin_tests`; it is the
second part of the 'magic' mechanism mentioned above.

#### plugin_formats

The hook function which will be called by jinjanator to allow this
plugin to register any format functions it provides; the
`@plugin_formats_hook` decorator marks the function so that it will be
found.

The function must return a dictionary, with each key being a format
function name (the name which will be used in the `--format` argument
to jinjanator, if needed) and the corresponding value being a class
which implements the requirements of the `Format` protocol (defined in
[__init__.py](src/jinjanator_plugins/__init__.py)).

In particular these requirements include:

* a class attribute called `name` which contains the name of the
  format (for use in error messages)

* a class attribute called 'suffixes' which contains a (possibly
  empty) list of file suffixes which can be matched to this format
  during format auto-detection

* a class attribute called 'option_names' which contains a (possibly
  empty) list of options which the user can provide to modify the
  parser's behavior

* a constructor method (`__init__`) which accepts a (possibly empty)
  list of options provided by the user, and performs any validation
  needed on them, storing the results in the `self` object

* a `parse` method which accepts a (possibly empty) string containing
  the input data, and parses it according to the format's needs, using
  any previously-validated options stored in the `self` object

Note that the hook function *must* be named `plugin_formats`; it is the
second part of the 'magic' mechanism mentioned above.

Format classes can accept 'options' to modify their behavior, and
should raise the exceptions listed below, when needed, to inform the
user if one of the provided options does not meet the format's
requirements.

* `FormatOptionUnknownError` will be raised automatically by the
  jinjanator CLI based on the content of the `option_names` attribute of
  the format class.

* `FormatOptionUnsupportedError` should be raised when a provided
  option is not supported in combination with the other provided
  options or with the parsed data.

* `FormatOptionValueError` should be raised when a provided option has
  a value that is not valid.

#### plugin_extensions

The hook function which will be called by jinjanator to allow this
plugin to register any additional Jinja2 extensions; the
`@plugin_extensions_hook` decorator marks the function so that it will be
found.

The function must return a list, with each entry being a string (the name
of a Jinja2 extension that should be added to the Jinja2 Environment).

Those strings should correspond to extensions that themselves are available
in your python installation and available for Jinja2 to locate.

Some examples:
* Jinja2 own debug extension: `jinja2.ext.debug`
* [Jinja-Markdown](https://github.com/jpsca/jinja-markdown): `jinja_markdown.MarkdownExtension`
* [jinja-markdown2](https://github.com/mkbabb/jinja-markdown2): `jinja2_markdown.MarkdownExtension`
* https://github.com/topics/jinja2-extension etc...

Note that the function *must* be named `plugin_extensions`; it is the
second part of the 'magic' mechanism mentioned above.
<!-- fancy-readme end -->

## Chat

If you'd like to chat with the jinjanator community, join us on
[Matrix](https://matrix.to/#/#jinjanator:km6g.us)!

## Credits

["Standing on the shoulders of
giants"](https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants)
could not be more true than it is in the Python community; this
project relies on many wonderful tools and libraries produced by the
global open source software community, in addition to Python
itself. I've listed many of them below, but if I've overlooked any
please do not be offended :-)

* [Attrs](https://pypi.org/project/attrs)
* [Black](https://pypi.org/project/black)
* [Hatch-Fancy-PyPI-Readme](https://pypi.org/project/hatch-fancy-pypi-readme)
* [Hatch](https://pypi.org/project/hatch)
* [Mypy](https://pypi.org/project/mypy)
* [Pluggy](https://pypi.org/project/pluggy)
* [pyproject-fmt](https://pypi.org/project/pyproject-fmt)
* [Pytest](https://pypi.org/project/pytest)
* [Ruff](https://pypi.org/project/ruff)
* [Towncrier](https://pypi.org/project/towncrier)
