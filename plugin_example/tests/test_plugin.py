from __future__ import annotations

from pathlib import Path

import pytest

from jinjanator.cli import render_command

from jinjanator_plugins import (
    FormatOptionUnknownError,
    FormatOptionUnsupportedError,
    FormatOptionValueError,
)


def test_filter(tmp_path: Path) -> None:
    template_file = tmp_path / "template.j2"
    template_file.write_text("{{ name | rot13 }}")
    data_file = tmp_path / "data.env"
    data_file.write_text("name=Bart")
    assert "Oneg" == render_command(
        Path.cwd(),
        {},
        None,
        ["", str(template_file), str(data_file)],
    )


def test_test(tmp_path: Path) -> None:
    template_file = tmp_path / "template.j2"
    template_file.write_text("{% if name is len12 %}pass{% endif %}")
    data_file = tmp_path / "data.env"
    data_file.write_text("name=Bartholomew1")
    assert "pass" == render_command(
        Path.cwd(),
        {},
        None,
        ["", str(template_file), str(data_file)],
    )


def test_format(tmp_path: Path) -> None:
    template_file = tmp_path / "template.j2"
    template_file.write_text("{{ cheese }}")
    data_file = tmp_path / "data.spam"
    data_file.write_text("")
    assert "spam and cheese" == render_command(
        Path.cwd(),
        {},
        None,
        ["", str(template_file), str(data_file)],
    )


def test_format_option(tmp_path: Path) -> None:
    template_file = tmp_path / "template.j2"
    template_file.write_text("{{ cheese }}")
    data_file = tmp_path / "data.spam"
    data_file.write_text("")
    assert "ham and cheese" == render_command(
        Path.cwd(),
        {},
        None,
        ["", "--format-option", "ham", str(template_file), str(data_file)],
    )


def test_format_option_unknown(tmp_path: Path) -> None:
    template_file = tmp_path / "template.j2"
    template_file.write_text("{{ cheese }}")
    data_file = tmp_path / "data.spam"
    data_file.write_text("")
    with pytest.raises(FormatOptionUnknownError):
        render_command(
            Path.cwd(),
            {},
            None,
            ["", "--format-option", "unk", str(template_file), str(data_file)],
        )


def test_format_option_unsupported(tmp_path: Path) -> None:
    template_file = tmp_path / "template.j2"
    template_file.write_text("{{ cheese }}")
    data_file = tmp_path / "data.spam"
    data_file.write_text("")
    with pytest.raises(FormatOptionUnsupportedError):
        render_command(
            Path.cwd(),
            {},
            None,
            ["", "--format-option", "uns", str(template_file), str(data_file)],
        )


def test_format_option_value(tmp_path: Path) -> None:
    template_file = tmp_path / "template.j2"
    template_file.write_text("{{ cheese }}")
    data_file = tmp_path / "data.spam"
    data_file.write_text("")
    with pytest.raises(FormatOptionValueError):
        render_command(
            Path.cwd(),
            {},
            None,
            ["", "--format-option", "val", str(template_file), str(data_file)],
        )
