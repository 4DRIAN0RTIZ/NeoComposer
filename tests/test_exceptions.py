import pytest

from neocomposer.exceptions import (
    ComposeError,
    ConfigError,
    ContactsError,
    NeoComposerError,
    SendError,
    TemplateError,
)


@pytest.mark.parametrize(
    "exc_cls",
    [ConfigError, ContactsError, ComposeError, SendError, TemplateError],
)
def test_domain_errors_are_neocomposer_errors(exc_cls):
    assert issubclass(exc_cls, NeoComposerError)


def test_neocomposer_error_is_exception():
    assert issubclass(NeoComposerError, Exception)


def test_domain_error_carries_message():
    err = ConfigError("missing field")
    assert str(err) == "missing field"
