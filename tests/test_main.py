import argparse
from unittest.mock import MagicMock, patch

import pytest

from neocomposer import main as main_module


def make_args(**overrides):
    defaults = dict(
        interactive=False,
        recipient=None,
        subject=None,
        body=None,
        body_file=None,
        attachments=None,
        template=None,
        template_var=[],
        contact_index=None,
        list_contacts=False,
        list_templates=False,
        open_contacts=False,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class TestBuildParser:
    def test_defaults(self):
        parser = main_module.build_parser()
        args = parser.parse_args([])
        assert args.interactive is False
        assert args.recipient is None
        assert args.template_var == []

    def test_parses_programmatic_flags(self):
        parser = main_module.build_parser()
        args = parser.parse_args(
            [
                "--recipient",
                "you@example.com",
                "--subject",
                "Hi",
                "--attachments",
                "a.txt",
                "b.txt",
                "-V",
                "name=Ada",
                "-V",
                "place=Earth",
            ]
        )
        assert args.recipient == "you@example.com"
        assert args.subject == "Hi"
        assert args.attachments == ["a.txt", "b.txt"]
        assert args.template_var == ["name=Ada", "place=Earth"]

    def test_contact_index_is_int(self):
        parser = main_module.build_parser()
        args = parser.parse_args(["--contact-index", "3"])
        assert args.contact_index == 3


class TestParseTemplateVars:
    def test_empty_list(self):
        assert main_module.parse_template_vars([]) == {}

    def test_single_var(self):
        assert main_module.parse_template_vars(["name=Ada"]) == {"name": "Ada"}

    def test_value_with_equals_sign(self):
        assert main_module.parse_template_vars(["url=http://a.com?x=1"]) == {
            "url": "http://a.com?x=1"
        }

    def test_strips_key_whitespace(self):
        assert main_module.parse_template_vars([" name =Ada"]) == {"name": "Ada"}

    def test_missing_equals_raises(self):
        with pytest.raises(ValueError, match="expected KEY=VALUE"):
            main_module.parse_template_vars(["invalid"])

    def test_empty_key_raises(self):
        with pytest.raises(ValueError, match="key cannot be empty"):
            main_module.parse_template_vars(["=value"])


class TestFormatTemplates:
    @patch("neocomposer.main.TemplatesManager")
    def test_no_templates(self, mock_manager_cls):
        manager = mock_manager_cls.return_value
        manager.list_templates.return_value = []
        manager.templates_dir = "/tpl"

        assert main_module.format_templates() == "No templates found in /tpl"

    @patch("neocomposer.main.TemplatesManager")
    def test_with_templates(self, mock_manager_cls):
        template = MagicMock()
        template.name = "welcome"
        template.subject = "Hi"
        template.variables = ["name"]

        manager = mock_manager_cls.return_value
        manager.list_templates.return_value = [template]

        result = main_module.format_templates()

        assert result == "Templates:\n1. welcome — Hi — vars: name"

    @patch("neocomposer.main.TemplatesManager")
    def test_template_without_subject(self, mock_manager_cls):
        template = MagicMock()
        template.name = "welcome"
        template.subject = None
        template.variables = []

        manager = mock_manager_cls.return_value
        manager.list_templates.return_value = [template]

        result = main_module.format_templates()

        assert result == "Templates:\n1. welcome — (No subject) — vars: none"


class TestHandleUtilityFlags:
    def test_no_flags_returns_false(self):
        assert main_module.handle_utility_flags(make_args()) is False

    @patch("neocomposer.main.paths.get_contacts_script_path")
    @patch("neocomposer.main.os.path.exists")
    @patch("neocomposer.main.os.system")
    def test_open_contacts_runs_script(self, mock_system, mock_exists, mock_path):
        mock_path.return_value = "/scripts/contacts.sh"
        mock_exists.return_value = True

        result = main_module.handle_utility_flags(make_args(open_contacts=True))

        assert result is True
        mock_system.assert_called_once_with("/scripts/contacts.sh")

    @patch("neocomposer.main.paths.get_contacts_script_path")
    @patch("neocomposer.main.os.path.exists")
    def test_open_contacts_missing_script_exits(self, mock_exists, mock_path):
        mock_path.return_value = "/scripts/contacts.sh"
        mock_exists.return_value = False

        with pytest.raises(SystemExit) as exc_info:
            main_module.handle_utility_flags(make_args(open_contacts=True))
        assert exc_info.value.code == 1

    @patch("neocomposer.main.ContactsManager")
    def test_list_contacts_prints_and_returns_true(self, mock_manager_cls, capsys):
        manager = mock_manager_cls.return_value
        manager.format_contacts.return_value = "Contacts:\n1. Ada"

        result = main_module.handle_utility_flags(make_args(list_contacts=True))

        assert result is True
        assert "Contacts:\n1. Ada" in capsys.readouterr().out

    @patch("neocomposer.main.ContactsManager")
    def test_list_contacts_error_exits(self, mock_manager_cls):
        mock_manager_cls.side_effect = Exception("boom")

        with pytest.raises(SystemExit) as exc_info:
            main_module.handle_utility_flags(make_args(list_contacts=True))
        assert exc_info.value.code == 1

    @patch("neocomposer.main.format_templates")
    def test_list_templates_prints_and_returns_true(self, mock_format, capsys):
        mock_format.return_value = "Templates:\n1. welcome"

        result = main_module.handle_utility_flags(make_args(list_templates=True))

        assert result is True
        assert "Templates:\n1. welcome" in capsys.readouterr().out

    @patch("neocomposer.main.format_templates")
    def test_list_templates_error_exits(self, mock_format):
        mock_format.side_effect = Exception("boom")

        with pytest.raises(SystemExit) as exc_info:
            main_module.handle_utility_flags(make_args(list_templates=True))
        assert exc_info.value.code == 1


class TestRun:
    def test_invalid_template_var_exits(self):
        args = make_args(template_var=["invalid"])
        with pytest.raises(SystemExit) as exc_info:
            main_module.run(args)
        assert exc_info.value.code == 1

    def test_programmatic_without_recipient_or_index_exits(self, capsys):
        args = make_args(subject="Hi")
        with pytest.raises(SystemExit) as exc_info:
            main_module.run(args)
        assert exc_info.value.code == 1
        assert "recipient or --contact-index" in capsys.readouterr().out

    @patch("neocomposer.main.EmailClient")
    def test_programmatic_mode_runs_client(self, mock_client_cls):
        args = make_args(recipient="you@example.com", subject="Hi")

        main_module.run(args)

        mock_client_cls.assert_called_once()
        mock_client_cls.return_value.run.assert_called_once()

    @patch("neocomposer.main.EmailClient")
    def test_programmatic_mode_reads_body_file(self, mock_client_cls, tmp_path):
        body_file = tmp_path / "body.txt"
        body_file.write_text("file body")
        args = make_args(recipient="you@example.com", body_file=str(body_file))

        main_module.run(args)

        _, kwargs = mock_client_cls.call_args
        assert kwargs["body"] == "file body"

    def test_programmatic_mode_missing_body_file_exits(self):
        args = make_args(recipient="you@example.com", body_file="/nonexistent.txt")
        with pytest.raises(SystemExit) as exc_info:
            main_module.run(args)
        assert exc_info.value.code == 1

    @patch("neocomposer.main.EmailClient")
    def test_programmatic_mode_client_error_exits(self, mock_client_cls):
        mock_client_cls.return_value.run.side_effect = Exception("send failed")
        args = make_args(recipient="you@example.com")

        with pytest.raises(SystemExit) as exc_info:
            main_module.run(args)
        assert exc_info.value.code == 1

    @patch("neocomposer.main.EmailClient")
    def test_interactive_mode_default(self, mock_client_cls):
        args = make_args()

        main_module.run(args)

        mock_client_cls.return_value.run_interactive.assert_called_once()

    @patch("neocomposer.main.EmailClient")
    def test_interactive_mode_keyboard_interrupt(self, mock_client_cls):
        mock_client_cls.return_value.run_interactive.side_effect = KeyboardInterrupt()
        args = make_args()

        with pytest.raises(SystemExit) as exc_info:
            main_module.run(args)
        assert exc_info.value.code == 130

    @patch("neocomposer.main.EmailClient")
    def test_interactive_mode_unexpected_error_exits(self, mock_client_cls):
        mock_client_cls.return_value.run_interactive.side_effect = RuntimeError("boom")
        args = make_args()

        with pytest.raises(SystemExit) as exc_info:
            main_module.run(args)
        assert exc_info.value.code == 1

    @patch("neocomposer.main.EmailClient")
    def test_explicit_interactive_flag_is_not_programmatic(self, mock_client_cls):
        args = make_args(interactive=True, recipient="you@example.com")

        main_module.run(args)

        mock_client_cls.return_value.run_interactive.assert_called_once()


class TestMainEntrypoint:
    @patch("neocomposer.main.run")
    @patch("neocomposer.main.handle_utility_flags", return_value=True)
    @patch("neocomposer.main.build_parser")
    def test_main_stops_after_utility_flag(
        self, mock_build_parser, mock_handle, mock_run
    ):
        mock_build_parser.return_value.parse_args.return_value = make_args()

        main_module.main()

        mock_handle.assert_called_once()
        mock_run.assert_not_called()

    @patch("neocomposer.main.run")
    @patch("neocomposer.main.handle_utility_flags", return_value=False)
    @patch("neocomposer.main.build_parser")
    def test_main_calls_run_when_no_utility_flag(
        self, mock_build_parser, mock_handle, mock_run
    ):
        args = make_args()
        mock_build_parser.return_value.parse_args.return_value = args

        main_module.main()

        mock_run.assert_called_once_with(args)
