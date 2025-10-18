# Changelog

All notable changes to this project will be documented in this file.

The format is based on [*Keep a
Changelog*](https://keepachangelog.com/en/1.0.0/) and this project
adheres to [*Calendar Versioning*](https://calver.org/).

The **first number** of the version is the year.

The **second number** is incremented with each release, starting at 1
for each year.

The **third number** is when we need to start branches for older
releases (only for emergencies).

Committed changes for the next release can be found in the ["changelog.d"
directory](https://github.com/kpfleming/jinjanator-plugins/tree/main/changelog.d)
in the project repository.

<!--
Do *NOT* add changelog entries here!

This changelog is managed by towncrier and is compiled at release time.

See https://github.com/kpfleming/jinjanator-plugins/blob/main/.github/CONTRIBUTING.md#changelog for details.
-->

<!-- towncrier release notes start -->

## [25.1.0](https://github.com/kpfleming/jinjanator-plugins/tree/25.1.0) - 2025-10-18

### Backwards-incompatible Changes

- Support for Python 3.9 has been removed, and support for Python 3.14
  has been added. Since the minimum supported version is now 3.10, the
  code has been updated to use features introduced in that version.
  


### Additions

- Added testing against Python 3.13 (again).
  

## [24.2.0](https://github.com/kpfleming/jinjanator-plugins/tree/24.2.0) - 2024-10-13

### Backwards-incompatible Changes

- Added support for Python 3.13, and removed support for Python 3.8.
  

## [24.1.0](https://github.com/kpfleming/jinjanator-plugins/tree/24.1.0) - 2024-03-19

### Additions

- Support for 'extensions' plugins which enable Jinja2 extensions (contributed by @llange)
  [#14](https://github.com/kpfleming/jinjanator-plugins/issues/14)

## [23.5.0](https://github.com/kpfleming/jinjanator-plugins/tree/23.5.0) - 2023-10-07

### Additions

- Added Python 3.12 support.
  [#9](https://github.com/kpfleming/jinjanator-plugins/issues/9)


## [23.4.0](https://github.com/kpfleming/jinjanator-plugins/tree/23.4.0) - 2023-08-01

### Backwards-incompatible Changes

- Major redesign of the 'formats' API; formats are now classes and can store data for their needs.
  [#4](https://github.com/kpfleming/jinjanator-plugins/issues/4)


## [23.3.0](https://github.com/kpfleming/jinjanator-plugins/tree/23.3.0) - 2023-08-01

### Changes

- Improved format option exceptions to accept details and messages, and provide their own formatted output.


## [23.2.1](https://github.com/kpfleming/jinjanator-plugins/tree/23.2.1) - 2023-07-31

### Additions

- Add documentation for features added in version 23.2.0.


## [23.2.0](https://github.com/kpfleming/jinjanator-plugins/tree/23.2.0) - 2023-07-30

### Additions

- Added hook for plugins to report their identities.
  [#1](https://github.com/kpfleming/jinjanator-plugins/issues/1)
- Added three exceptions which Format plugins can raise to indicate problems with options provided to them.
  [#2](https://github.com/kpfleming/jinjanator-plugins/issues/2)


### Changes

- Converted tests to proper unit tests.


## [23.1.0](https://github.com/kpfleming/jinjanator-plugins/tree/23.1.0) - 2023-07-24

Initial release!
