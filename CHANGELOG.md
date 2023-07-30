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
