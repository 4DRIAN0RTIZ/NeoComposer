import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional

from .exceptions import ComposeError


class MailComposer:
    """Composes MIME messages with HTML body, signature, and attachments"""

    def __init__(self, signature_path: Optional[str] = None):
        """
        Args:
            signature_path: Path to the HTML signature file. If not specified,
                uses signature.html next to this module (independent of cwd).
        """
        self.signature_path = signature_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "signature.html"
        )
        self.signature_content = self._load_signature()

    def _load_signature(self) -> str:
        """Loads the HTML signature if it exists"""
        if not os.path.exists(self.signature_path):
            return ""
        try:
            with open(self.signature_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Warning: could not read signature ({self.signature_path}): {e}")
            return ""

    def compose(
        self,
        subject: str,
        sender_name: str,
        sender_email: str,
        recipient: str,
        body_html: str,
    ) -> MIMEMultipart:
        """
        Creates the base MIME message with headers and HTML body

        Args:
            subject: Email subject
            sender_name: Sender name
            sender_email: Sender email
            recipient: Recipient email
            body_html: Message body in HTML
        """
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = f"{sender_name} <{sender_email}>"
        message["To"] = recipient

        # Attach HTML body with signature
        full_body = body_html + self.signature_content
        text_part = MIMEText(full_body, "html")
        message.attach(text_part)

        return message

    def add_attachment(self, message: MIMEMultipart, file_path: str) -> None:
        """
        Attaches a file to an existing message

        Args:
            message: MIME message to add the attachment to
            file_path: Full path of the file to attach
        """
        try:
            with open(file_path, "rb") as attachment:
                attachment_part = MIMEBase("application", "octet-stream")
                attachment_part.set_payload(attachment.read())
                encoders.encode_base64(attachment_part)
                attachment_part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(file_path)}",
                )
                message.attach(attachment_part)
        except FileNotFoundError:
            raise ComposeError(f"Attachment file not found: {file_path}")
        except Exception as e:
            raise ComposeError(f"Error attaching file {file_path}: {str(e)}")
