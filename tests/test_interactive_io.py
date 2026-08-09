from unittest.mock import MagicMock, patch

import pytest

from neocomposer import interactive_io
from neocomposer.exceptions import ContactsError


@patch("neocomposer.interactive_io.os.system")
def test_compose_body_with_neovim_captures_content(mock_system, tmp_path):
    captured_path = {}

    def fake_system(cmd):
        path = cmd.split(" ", 1)[1]
        captured_path["path"] = path
        with open(path, "w", encoding="utf-8") as f:
            f.write("edited body")

    mock_system.side_effect = fake_system

    result = interactive_io.compose_body_with_neovim("initial")

    assert result == "edited body"
    mock_system.assert_called_once()
    assert not __import__("os").path.exists(captured_path["path"])


@patch("neocomposer.interactive_io.os.system")
def test_select_file_with_yazi_strips_result(mock_system):
    def fake_system(cmd):
        path = cmd.split("=", 1)[1]
        with open(path, "w", encoding="utf-8") as f:
            f.write("  /tmp/chosen.txt  \n")

    mock_system.side_effect = fake_system

    result = interactive_io.select_file_with_yazi()

    assert result == "/tmp/chosen.txt"


def test_prompt_recipient_manual_entry(monkeypatch):
    inputs = iter(["1", "someone@example.com"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = interactive_io.prompt_recipient(MagicMock())

    assert result == "someone@example.com"


def test_prompt_recipient_from_contacts(monkeypatch):
    contacts = MagicMock()
    contacts.format_contacts.return_value = "Contacts:\n1. Ada (ada@example.com)"
    contacts.get_contact_by_index.return_value = MagicMock(email="ada@example.com")

    inputs = iter(["2", "1"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = interactive_io.prompt_recipient(contacts)

    assert result == "ada@example.com"


def test_prompt_recipient_retries_on_invalid_selection(monkeypatch):
    contacts = MagicMock()
    contacts.format_contacts.return_value = "Contacts:"
    contacts.get_contact_by_index.side_effect = [
        ContactsError("Invalid index. Must be between 1 and 1"),
        MagicMock(email="ada@example.com"),
    ]

    inputs = iter(["2", "9", "1"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = interactive_io.prompt_recipient(contacts)

    assert result == "ada@example.com"


def test_prompt_recipient_invalid_option_raises(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "3")

    with pytest.raises(ContactsError, match="Invalid option"):
        interactive_io.prompt_recipient(MagicMock())


def test_prompt_template_declines(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "n")
    assert interactive_io.prompt_template(MagicMock()) is None


def test_prompt_template_selects_by_number(monkeypatch):
    templates_manager = MagicMock()
    template = MagicMock(name="welcome", subject="Hi", path="/tpl/welcome.txt")
    template.variables = ["name"]
    templates_manager.list_templates.return_value = [template]

    inputs = iter(["y", "1"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = interactive_io.prompt_template(templates_manager)

    assert result == "/tpl/welcome.txt"


def test_prompt_template_no_templates_available(monkeypatch):
    templates_manager = MagicMock()
    templates_manager.list_templates.return_value = []
    templates_manager.templates_dir = "/tpl"

    inputs = iter(["y", "custom-name"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = interactive_io.prompt_template(templates_manager)

    assert result == "custom-name"


def test_prompt_template_empty_selection_skips(monkeypatch):
    templates_manager = MagicMock()
    templates_manager.list_templates.return_value = []
    templates_manager.templates_dir = "/tpl"

    inputs = iter(["y", ""])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    assert interactive_io.prompt_template(templates_manager) is None


def test_prompt_template_vars_fills_missing_only(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "Ada")

    result = interactive_io.prompt_template_vars(
        ["name", "place"], {"place": "Earth"}
    )

    assert result == {"place": "Earth", "name": "Ada"}


def test_prompt_attachments_collects_files(monkeypatch):
    inputs = iter(["y", "y", "n"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))
    monkeypatch.setattr(
        interactive_io, "select_file_with_yazi", lambda: "/tmp/file.txt"
    )

    result = interactive_io.prompt_attachments()

    assert result == ["/tmp/file.txt", "/tmp/file.txt"]


def test_prompt_attachments_declines_immediately(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "n")
    assert interactive_io.prompt_attachments() == []


def test_prompt_attachments_handles_selection_error(monkeypatch, capsys):
    inputs = iter(["y", "n"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    def raise_error():
        raise RuntimeError("yazi not found")

    monkeypatch.setattr(interactive_io, "select_file_with_yazi", raise_error)

    result = interactive_io.prompt_attachments()

    assert result == []
    assert "Error selecting file" in capsys.readouterr().out


@patch("neocomposer.interactive_io.os.system")
def test_clear_screen(mock_system):
    interactive_io.clear_screen()
    mock_system.assert_called_once_with("clear")


@patch("neocomposer.interactive_io.time.sleep")
def test_show_sending_animation(mock_sleep, capsys):
    interactive_io.show_sending_animation(0.1, ["|"])
    assert mock_sleep.called
    assert "Sending email..." in capsys.readouterr().out


@pytest.mark.parametrize(
    "success, programmatic, expected",
    [
        (True, False, "✓ Email sent successfully"),
        (True, True, "✓ Email sent successfully (programmatic mode)"),
        (False, True, "✗ Error in programmatic send"),
        (False, False, "✗ An error occurred"),
    ],
)
def test_print_send_result(success, programmatic, expected, capsys):
    interactive_io.print_send_result(success, programmatic=programmatic)
    assert capsys.readouterr().out.strip() == expected
