import os
import sys
from typing import Dict, Optional, List, Tuple
from .config_manager import ConfigManager
from .contacts_manager import ContactsManager
from .mail_composer import MailComposer
from .mail_sender import MailSender
from .templates_manager import TemplatesManager

from . import interactive_io
from . import paths
from .exceptions import NeoComposerError


class EmailClient:
    """Main orchestrator with interactive and programmatic modes"""

    def __init__(
        self,
        recipient: Optional[str] = None,
        subject: Optional[str] = None,
        body: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        contact_index: Optional[int] = None,
        template: Optional[str] = None,
        template_vars: Optional[Dict[str, str]] = None,
    ):
        """
        Args:
            recipient: Recipient email (programmatic mode)
            subject: Subject (programmatic mode)
            body: Message body (programmatic mode)
            attachments: List of files to attach (programmatic mode)
            contact_index: Contact index in the contacts list (1-indexed, programmatic mode)
            template: Reusable email template name or path (programmatic mode)
            template_vars: Values used to render template placeholders
        """
        self.config_path = paths.get_env_path()
        self.contacts_path = paths.get_contacts_path()
        self._config_manager = ConfigManager(self.config_path)
        self._composer = MailComposer()
        self._templates_manager = TemplatesManager()

        # Programmatic mode
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.contact_index = contact_index
        self.template = template
        self.template_vars = template_vars or {}
        self._is_programmatic = any(
            [recipient, subject, body, attachments, contact_index, template]
        )

    def _render_template(
        self,
        recipient: str,
        subject: Optional[str],
        body: Optional[str],
    ) -> Tuple[Optional[str], str]:
        """Renders the configured template and applies CLI precedence rules."""
        if not self.template:
            return subject, body or ""

        variables = dict(self.template_vars)
        variables.setdefault("recipient", recipient)
        if subject is not None:
            variables.setdefault("subject", subject)
        if body is not None:
            variables.setdefault("body", body)

        template_subject, template_body = self._templates_manager.render(
            self.template, variables
        )
        return subject or template_subject, template_body

    def _compose_and_send(
        self,
        config: dict,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        before_send=None,
    ) -> bool:
        """Composes the message, attaches files, and sends it. Shared between
        the programmatic and interactive flows.

        before_send, if passed, is invoked with the already-built MailSender
        right before sending (used by interactive mode to show the loading
        animation without duplicating the sender construction)."""
        message = self._composer.compose(
            subject=subject,
            sender_name=config["sender_name"],
            sender_email=config["sender_email"],
            recipient=recipient,
            body_html=body.replace("\n", "<br>") if body else "",
        )

        for file_path in attachments or []:
            if os.path.exists(file_path):
                self._composer.add_attachment(message, file_path)
            else:
                print(f"Warning: File not found {file_path}")

        sender = MailSender(
            smtp_server=config["smtp_server"],
            smtp_port=config["smtp_port"],
            sender_email=config["sender_email"],
            sender_password=config["sender_password"],
        )

        if before_send:
            before_send(sender)

        return sender.send(message, recipient)

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
    ) -> bool:
        """
        Programmatic email send

        Args:
            recipient: Recipient email
            subject: Message subject
            body: Message body (can be plaintext)
            attachments: Optional list of file paths

        Returns:
            bool: True if the send was successful

        Raises:
            Exception: If there is an error in configuration, composition, or sending
        """
        config = self._config_manager.load()
        return self._compose_and_send(config, recipient, subject, body, attachments)

    def run_interactive(self) -> None:
        """Runs the interactive flow"""
        interactive_io.clear_screen()

        config = self._config_manager.load()

        contacts = ContactsManager(self.contacts_path)
        recipient = interactive_io.prompt_recipient(contacts)

        selected_template = self.template or interactive_io.prompt_template(
            self._templates_manager
        )
        if selected_template:
            self.template = selected_template
            template = self._templates_manager.load(selected_template)
            variables = dict(self.template_vars)
            variables.setdefault("recipient", recipient)
            variables = interactive_io.prompt_template_vars(template.variables, variables)
            self.template_vars = variables
            template_subject, template_body = self._render_template(
                recipient=recipient,
                subject=None,
                body=None,
            )
            if template_subject:
                subject_override = input(f"Subject [{template_subject}]: ").strip()
                subject = subject_override or template_subject
            else:
                subject = input("Subject: ").strip()
            body = interactive_io.compose_body_with_neovim(template_body)
        else:
            subject = input("Subject: ").strip()
            body = interactive_io.compose_body_with_neovim()

        attachments = interactive_io.prompt_attachments()

        success = self._compose_and_send(
            config,
            recipient=recipient,
            subject=subject,
            body=body,
            attachments=attachments,
            before_send=lambda sender: interactive_io.show_sending_animation(
                1, ["|", "/", "-", "\\"]
            ),
        )

        interactive_io.print_send_result(success, programmatic=False)

    def run(self) -> None:
        """Detects mode and runs the corresponding flow"""
        try:
            if self._is_programmatic:
                # Programmatic mode
                recipient = self.recipient

                if self.contact_index:
                    contacts = ContactsManager(self.contacts_path)
                    contact = contacts.get_contact_by_index(self.contact_index)
                    recipient = contact.email

                subject, body = self._render_template(
                    recipient=recipient,
                    subject=self.subject,
                    body=self.body,
                )

                success = self.send_email(
                    recipient=recipient,
                    subject=subject or "(No subject)",
                    body=body,
                    attachments=self.attachments,
                )

                interactive_io.print_send_result(success, programmatic=True)
                if not success:
                    sys.exit(1)

            else:
                # Interactive mode
                self.run_interactive()

        except NeoComposerError as e:
            print(f"\nError: {str(e)}")
            sys.exit(1)
        except Exception as e:
            print(f"\nCritical error: {str(e)}")
            import traceback

            traceback.print_exc()
            sys.exit(1)
