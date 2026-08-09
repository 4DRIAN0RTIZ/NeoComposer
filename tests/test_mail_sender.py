import smtplib
from unittest.mock import MagicMock, patch

import pytest

from neocomposer.mail_sender import MailSender


@pytest.fixture
def sender():
    return MailSender(
        smtp_server="smtp.example.com",
        smtp_port=587,
        sender_email="me@example.com",
        sender_password="secret",
    )


@pytest.fixture
def fake_message():
    message = MagicMock()
    message.as_string.return_value = "raw-mime-string"
    return message


@patch("neocomposer.mail_sender.smtplib.SMTP")
def test_send_success(mock_smtp_cls, sender, fake_message):
    smtp = mock_smtp_cls.return_value
    smtp.sendmail.return_value = {}
    smtp.noop.return_value = (250, b"OK")

    result = sender.send(fake_message, "you@example.com")

    assert result is True
    mock_smtp_cls.assert_called_once_with("smtp.example.com", 587)
    smtp.starttls.assert_called_once()
    smtp.login.assert_called_once_with("me@example.com", "secret")
    smtp.sendmail.assert_called_once_with(
        "me@example.com", "you@example.com", "raw-mime-string"
    )
    smtp.quit.assert_called_once()


@patch("neocomposer.mail_sender.smtplib.SMTP")
def test_send_noop_failure_returns_false(mock_smtp_cls, sender, fake_message):
    smtp = mock_smtp_cls.return_value
    smtp.noop.return_value = (421, b"Service unavailable")

    result = sender.send(fake_message, "you@example.com")

    assert result is False


@patch("neocomposer.mail_sender.smtplib.SMTP")
def test_connect_raises_connection_error_on_smtp_exception(mock_smtp_cls, sender, fake_message):
    smtp = mock_smtp_cls.return_value
    smtp.login.side_effect = smtplib.SMTPAuthenticationError(535, b"bad credentials")

    with pytest.raises(ConnectionError, match="SMTP authentication error"):
        sender.send(fake_message, "you@example.com")

    smtp.quit.assert_called_once()


@patch("neocomposer.mail_sender.smtplib.SMTP")
def test_connect_quits_even_if_quit_raises(mock_smtp_cls, sender, fake_message):
    smtp = mock_smtp_cls.return_value
    smtp.quit.side_effect = Exception("already closed")
    smtp.noop.return_value = (250, b"OK")

    result = sender.send(fake_message, "you@example.com")

    assert result is True
