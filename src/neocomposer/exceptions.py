class NeoComposerError(Exception):
    """Base exception for NeoComposer domain errors"""


class ConfigError(NeoComposerError):
    """Configuration error (.env missing or invalid)"""


class ContactsError(NeoComposerError):
    """Error related to the contacts list"""


class ComposeError(NeoComposerError):
    """Error composing the MIME message"""


class SendError(NeoComposerError):
    """Error sending the message via SMTP"""
