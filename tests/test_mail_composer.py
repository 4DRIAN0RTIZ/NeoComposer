import pytest

from neocomposer.exceptions import ComposeError
from neocomposer.mail_composer import MailComposer


@pytest.fixture
def composer_no_signature(tmp_path):
    signature_path = tmp_path / "signature.html"
    return MailComposer(signature_path=str(signature_path))


@pytest.fixture
def composer_with_signature(tmp_path):
    signature_path = tmp_path / "signature.html"
    signature_path.write_text("<p>Best regards</p>")
    return MailComposer(signature_path=str(signature_path))


def test_load_signature_missing_file_is_empty(composer_no_signature):
    assert composer_no_signature.signature_content == ""


def test_load_signature_reads_existing_file(composer_with_signature):
    assert composer_with_signature.signature_content == "<p>Best regards</p>"


def test_default_signature_path_is_package_local():
    composer = MailComposer()
    assert composer.signature_path.endswith("signature.html")


def test_compose_sets_headers(composer_no_signature):
    message = composer_no_signature.compose(
        subject="Hello",
        sender_name="Me",
        sender_email="me@example.com",
        recipient="you@example.com",
        body_html="<p>Hi</p>",
    )

    assert message["Subject"] == "Hello"
    assert message["From"] == "Me <me@example.com>"
    assert message["To"] == "you@example.com"


def test_compose_appends_signature_to_body(composer_with_signature):
    message = composer_with_signature.compose(
        subject="Hello",
        sender_name="Me",
        sender_email="me@example.com",
        recipient="you@example.com",
        body_html="<p>Hi</p>",
    )

    body_part = message.get_payload()[0]
    payload = body_part.get_payload()
    assert payload == "<p>Hi</p><p>Best regards</p>"
    assert body_part.get_content_type() == "text/html"


def test_add_attachment_success(composer_no_signature, tmp_path):
    message = composer_no_signature.compose(
        subject="Hello",
        sender_name="Me",
        sender_email="me@example.com",
        recipient="you@example.com",
        body_html="<p>Hi</p>",
    )
    attachment_file = tmp_path / "report.txt"
    attachment_file.write_text("report contents")

    composer_no_signature.add_attachment(message, str(attachment_file))

    parts = message.get_payload()
    assert len(parts) == 2
    assert "report.txt" in parts[1]["Content-Disposition"]


def test_add_attachment_missing_file_raises(composer_no_signature):
    message = composer_no_signature.compose(
        subject="Hello",
        sender_name="Me",
        sender_email="me@example.com",
        recipient="you@example.com",
        body_html="<p>Hi</p>",
    )

    with pytest.raises(ComposeError, match="Attachment file not found"):
        composer_no_signature.add_attachment(message, "/nonexistent/path.txt")
