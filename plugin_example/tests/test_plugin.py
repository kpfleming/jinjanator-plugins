from __future__ import annotations

from pathlib import Path

from jinjanator.cli import render_command


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
