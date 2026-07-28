#!/usr/bin/env python3

import os
import sys
import argparse
from .email_client import EmailClient
from .contacts_manager import ContactsManager
from .templates_manager import TemplatesManager

from . import paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NeoComposer - Send emails from the terminal (interactive or programmatic)"
    )

    # Interactive mode (default)
    parser.add_argument(
        "--interactive",
        "-I",
        action="store_true",
        help="Interactive mode (default if no other args are passed)",
    )

    # Programmatic mode
    parser.add_argument(
        "--recipient",
        "-r",
        type=str,
        help="Recipient email (required in programmatic mode)",
    )

    parser.add_argument("--subject", "-s", type=str, help="Email subject")

    parser.add_argument(
        "--body", "-b", type=str, help="Message body (plain text or HTML)"
    )

    parser.add_argument(
        "--body-file", "-f", type=str, help="File containing the message body"
    )

    parser.add_argument(
        "--attachments",
        "-a",
        type=str,
        nargs="+",
        help="Files to attach (space separated)",
    )

    parser.add_argument(
        "--template",
        "-t",
        type=str,
        help="Reusable email template name or path",
    )

    parser.add_argument(
        "--template-var",
        "-V",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Template variable value (repeatable)",
    )

    parser.add_argument(
        "--contact-index",
        "-i",
        type=int,
        help="Contact index in the contacts list (1-indexed, uses the contacts list instead of --recipient)",
    )

    # Utilities
    parser.add_argument(
        "--list-contacts",
        "-l",
        action="store_true",
        help="List contacts and exit",
    )

    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List reusable email templates and exit",
    )

    parser.add_argument(
        "--open-contacts",
        "--contacts",
        action="store_true",
        help="Open the NeoComposer contacts list",
    )

    return parser


def parse_template_vars(raw_vars: list[str]) -> dict:
    """Parses repeated KEY=VALUE template variables from the CLI."""
    parsed = {}
    for raw_var in raw_vars:
        if "=" not in raw_var:
            raise ValueError(f"Invalid template variable '{raw_var}', expected KEY=VALUE")
        key, value = raw_var.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid template variable '{raw_var}', key cannot be empty")
        parsed[key] = value
    return parsed


def format_templates() -> str:
    """Formats the template list as readable console text."""
    manager = TemplatesManager()
    templates = manager.list_templates()
    if not templates:
        return f"No templates found in {manager.templates_dir}"

    lines = ["Templates:"]
    for index, template in enumerate(templates, 1):
        subject = template.subject or "(No subject)"
        variables = ", ".join(template.variables) or "none"
        lines.append(f"{index}. {template.name} — {subject} — vars: {variables}")
    return "\n".join(lines)


def handle_utility_flags(args: argparse.Namespace) -> bool:
    """Handles utility flags. Returns True if a utility was handled (the caller
    should stop execution in that case)."""
    if args.open_contacts:
        try:
            script_path = paths.get_contacts_script_path()
            if os.path.exists(script_path):
                os.system(script_path)
            else:
                print(f"Error: Contacts script not found: {script_path}")
                sys.exit(1)
        except Exception as e:
            print(f"Error running contacts script: {str(e)}")
            sys.exit(1)
        return True

    if args.list_contacts:
        try:
            contacts = ContactsManager(paths.get_contacts_path())
            print(contacts.format_contacts())
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
        return True

    if args.list_templates:
        try:
            print(format_templates())
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
        return True

    return False


def run(args: argparse.Namespace) -> None:
    try:
        template_vars = parse_template_vars(args.template_var)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    is_programmatic = not args.interactive and any(
        [
            args.recipient,
            args.subject,
            args.body,
            args.body_file,
            args.attachments,
            args.contact_index,
            args.template,
            args.template_var,
        ]
    )

    if is_programmatic:
        if not args.recipient and not args.contact_index:
            print("Error: You must specify --recipient or --contact-index")
            sys.exit(1)

        # Read body from file if specified
        body = args.body
        if args.body_file:
            try:
                with open(args.body_file, "r", encoding="utf-8") as f:
                    body = f.read()
            except Exception as e:
                print(f"Error reading body file: {str(e)}")
                sys.exit(1)

        try:
            client = EmailClient(
                recipient=args.recipient,
                subject=args.subject,
                body=body,
                attachments=args.attachments,
                contact_index=args.contact_index,
                template=args.template,
                template_vars=template_vars,
            )
            client.run()
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

    else:
        try:
            client = EmailClient(template=args.template, template_vars=template_vars)
            client.run_interactive()
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by the user")
            sys.exit(130)
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
            sys.exit(1)


def main():
    parser = build_parser()
    args = parser.parse_args()

    if handle_utility_flags(args):
        return

    run(args)


if __name__ == "__main__":
    main()
