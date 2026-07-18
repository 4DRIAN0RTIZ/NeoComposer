import smtplib
from email.mime.multipart import MIMEMultipart
from contextlib import contextmanager


class MailSender:
    """Handles SMTP connection and message sending"""

    def __init__(
        self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str
    ):
        """
        Args:
            smtp_server: SMTP server
            smtp_port: SMTP port
            sender_email: Sender email
            sender_password: Sender password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    @contextmanager
    def connect(self) -> smtplib.SMTP:
        """
        Context manager for secure SMTP connections

        Yields:
            smtplib.SMTP: Authenticated connection

        Raises:
            smtplib.SMTPException: If authentication fails
        """
        smtp = None
        try:
            smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp.starttls()
            smtp.login(self.sender_email, self.sender_password)
            yield smtp
        except smtplib.SMTPException as e:
            raise ConnectionError(f"SMTP authentication error: {str(e)}") from e
        finally:
            if smtp:
                try:
                    smtp.quit()
                except Exception:
                    pass

    def send(self, message: MIMEMultipart, recipient: str) -> bool:
        """
        Sends a message via SMTP

        Args:
            message: Composed MIME message
            recipient: Recipient email

        Returns:
            bool: True if successful

        Raises:
            Exception: If sending fails
        """
        with self.connect() as smtp:
            smtp.sendmail(self.sender_email, recipient, message.as_string())
            return smtp.noop()[0] == 250
