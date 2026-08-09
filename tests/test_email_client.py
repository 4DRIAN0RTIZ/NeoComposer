from unittest.mock import MagicMock, patch

import pytest

from neocomposer.email_client import EmailClient
from neocomposer.exceptions import NeoComposerError


@pytest.fixture(autouse=True)
def mocked_collaborators():
    with patch("neocomposer.email_client.paths") as mock_paths, patch(
        "neocomposer.email_client.ConfigManager"
    ) as mock_config_manager_cls, patch(
        "neocomposer.email_client.MailComposer"
    ) as mock_composer_cls, patch(
        "neocomposer.email_client.TemplatesManager"
    ) as mock_templates_cls, patch(
        "neocomposer.email_client.ContactsManager"
    ) as mock_contacts_cls, patch(
        "neocomposer.email_client.MailSender"
    ) as mock_sender_cls, patch(
        "neocomposer.email_client.interactive_io"
    ) as mock_io:
        mock_paths.get_env_path.return_value = "/fake/.env"
        mock_paths.get_contacts_path.return_value = "/fake/contacts.json"
        yield {
            "paths": mock_paths,
            "config_manager_cls": mock_config_manager_cls,
            "composer_cls": mock_composer_cls,
            "templates_cls": mock_templates_cls,
            "contacts_cls": mock_contacts_cls,
            "sender_cls": mock_sender_cls,
            "io": mock_io,
        }


class TestInit:
    def test_interactive_mode_when_no_fields_given(self, mocked_collaborators):
        client = EmailClient()
        assert client._is_programmatic is False

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"recipient": "you@example.com"},
            {"subject": "Hi"},
            {"body": "text"},
            {"attachments": ["a.txt"]},
            {"contact_index": 1},
            {"template": "welcome"},
        ],
    )
    def test_programmatic_mode_detected(self, mocked_collaborators, kwargs):
        client = EmailClient(**kwargs)
        assert client._is_programmatic is True

    def test_template_vars_default_to_empty_dict(self, mocked_collaborators):
        client = EmailClient()
        assert client.template_vars == {}


class TestRenderTemplate:
    def test_no_template_returns_subject_and_body(self, mocked_collaborators):
        client = EmailClient()
        subject, body = client._render_template("you@example.com", "Hi", "Body")
        assert subject == "Hi"
        assert body == "Body"

    def test_no_template_none_body_becomes_empty_string(self, mocked_collaborators):
        client = EmailClient()
        subject, body = client._render_template("you@example.com", "Hi", None)
        assert body == ""

    def test_with_template_delegates_to_templates_manager(self, mocked_collaborators):
        client = EmailClient(template="welcome")
        client._templates_manager.render.return_value = ("Rendered Subject", "Rendered Body")

        subject, body = client._render_template("you@example.com", None, None)

        assert subject == "Rendered Subject"
        assert body == "Rendered Body"
        args, _ = client._templates_manager.render.call_args
        assert args[0] == "welcome"
        assert args[1]["recipient"] == "you@example.com"

    def test_with_template_cli_subject_takes_precedence(self, mocked_collaborators):
        client = EmailClient(template="welcome")
        client._templates_manager.render.return_value = ("Template Subject", "Body")

        subject, _ = client._render_template("you@example.com", "CLI Subject", None)

        assert subject == "CLI Subject"


class TestComposeAndSend:
    def test_composes_and_sends_successfully(self, mocked_collaborators):
        client = EmailClient()
        client._composer.compose.return_value = MagicMock()
        mocked_collaborators["sender_cls"].return_value.send.return_value = True

        config = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }

        result = client._compose_and_send(config, "you@example.com", "Hi", "Body\nLine2")

        assert result is True
        client._composer.compose.assert_called_once_with(
            subject="Hi",
            sender_name="Me",
            sender_email="me@example.com",
            recipient="you@example.com",
            body_html="Body<br>Line2",
        )

    def test_adds_existing_attachments(self, mocked_collaborators, tmp_path):
        client = EmailClient()
        attachment = tmp_path / "file.txt"
        attachment.write_text("data")
        mocked_collaborators["sender_cls"].return_value.send.return_value = True

        config = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }

        client._compose_and_send(
            config, "you@example.com", "Hi", "Body", attachments=[str(attachment)]
        )

        client._composer.add_attachment.assert_called_once()

    def test_warns_on_missing_attachment(self, mocked_collaborators, capsys):
        client = EmailClient()
        mocked_collaborators["sender_cls"].return_value.send.return_value = True

        config = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }

        client._compose_and_send(
            config, "you@example.com", "Hi", "Body", attachments=["/missing.txt"]
        )

        client._composer.add_attachment.assert_not_called()
        assert "Warning: File not found /missing.txt" in capsys.readouterr().out

    def test_calls_before_send_hook(self, mocked_collaborators):
        client = EmailClient()
        mocked_collaborators["sender_cls"].return_value.send.return_value = True
        hook = MagicMock()

        config = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }

        client._compose_and_send(
            config, "you@example.com", "Hi", "Body", before_send=hook
        )

        hook.assert_called_once_with(mocked_collaborators["sender_cls"].return_value)


class TestSendEmail:
    def test_loads_config_and_sends(self, mocked_collaborators):
        client = EmailClient()
        client._config_manager.load.return_value = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }
        mocked_collaborators["sender_cls"].return_value.send.return_value = True

        result = client.send_email("you@example.com", "Hi", "Body")

        assert result is True
        client._config_manager.load.assert_called_once()


class TestRunInteractive:
    def test_no_template_flow(self, mocked_collaborators):
        io = mocked_collaborators["io"]
        client = EmailClient()
        client._config_manager.load.return_value = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }
        io.prompt_recipient.return_value = "you@example.com"
        io.prompt_template.return_value = None
        io.compose_body_with_neovim.return_value = "typed body"
        io.prompt_attachments.return_value = []
        mocked_collaborators["sender_cls"].return_value.send.return_value = True

        with patch("builtins.input", return_value="Hi"):
            client.run_interactive()

        io.clear_screen.assert_called_once()
        io.print_send_result.assert_called_once_with(True, programmatic=False)

    def test_template_flow(self, mocked_collaborators):
        io = mocked_collaborators["io"]
        client = EmailClient()
        client._config_manager.load.return_value = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }
        io.prompt_recipient.return_value = "you@example.com"
        io.prompt_template.return_value = "welcome"
        loaded_template = MagicMock()
        loaded_template.variables = ["name"]
        client._templates_manager.load.return_value = loaded_template
        io.prompt_template_vars.return_value = {"recipient": "you@example.com", "name": "Ada"}
        client._templates_manager.render.return_value = ("Rendered Subject", "Rendered Body")
        io.compose_body_with_neovim.return_value = "final body"
        io.prompt_attachments.return_value = []
        mocked_collaborators["sender_cls"].return_value.send.return_value = True

        with patch("builtins.input", return_value=""):
            client.run_interactive()

        io.compose_body_with_neovim.assert_called_once_with("Rendered Body")
        io.print_send_result.assert_called_once_with(True, programmatic=False)


class TestRun:
    def test_programmatic_success(self, mocked_collaborators):
        client = EmailClient(recipient="you@example.com", subject="Hi", body="Body")
        client._config_manager.load.return_value = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }
        mocked_collaborators["sender_cls"].return_value.send.return_value = True

        client.run()

        mocked_collaborators["io"].print_send_result.assert_called_once_with(
            True, programmatic=True
        )

    def test_programmatic_failure_exits(self, mocked_collaborators):
        client = EmailClient(recipient="you@example.com", subject="Hi", body="Body")
        client._config_manager.load.return_value = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }
        mocked_collaborators["sender_cls"].return_value.send.return_value = False

        with pytest.raises(SystemExit) as exc_info:
            client.run()
        assert exc_info.value.code == 1

    def test_programmatic_resolves_contact_index(self, mocked_collaborators):
        client = EmailClient(contact_index=1, subject="Hi", body="Body")
        client._config_manager.load.return_value = {
            "sender_name": "Me",
            "sender_email": "me@example.com",
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_password": "secret",
        }
        contact = MagicMock(email="ada@example.com")
        mocked_collaborators["contacts_cls"].return_value.get_contact_by_index.return_value = contact
        mocked_collaborators["sender_cls"].return_value.send.return_value = True

        client.run()

        mocked_collaborators["contacts_cls"].return_value.get_contact_by_index.assert_called_once_with(1)

    def test_neocomposer_error_exits_cleanly(self, mocked_collaborators, capsys):
        client = EmailClient(recipient="you@example.com", subject="Hi", body="Body")
        client._config_manager.load.side_effect = NeoComposerError("config broken")

        with pytest.raises(SystemExit) as exc_info:
            client.run()
        assert exc_info.value.code == 1
        assert "Error: config broken" in capsys.readouterr().out

    def test_unexpected_error_exits_with_traceback(self, mocked_collaborators, capsys):
        client = EmailClient(recipient="you@example.com", subject="Hi", body="Body")
        client._config_manager.load.side_effect = RuntimeError("boom")

        with pytest.raises(SystemExit) as exc_info:
            client.run()
        assert exc_info.value.code == 1
        assert "Critical error: boom" in capsys.readouterr().out

    def test_interactive_dispatches_to_run_interactive(self, mocked_collaborators):
        client = EmailClient()
        client.run_interactive = MagicMock()

        client.run()

        client.run_interactive.assert_called_once()
