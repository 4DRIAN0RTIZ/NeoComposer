# Configuration, contacts, and templates

This page covers the data files and runtime rules that drive NeoComposer. These are the areas most likely to matter when changing message content, local setup, or reusable mail snippets.

## Configuration

`src/neocomposer/config_manager.py` loads SMTP settings from the user config file at `~/.config/neocomposer/.env`. The loader requires these variables:

- `SMTP_SERVER`
- `SMTP_PORT`
- `SENDER_EMAIL`
- `SENDER_PASSWORD`
- `SENDER_NAME`

`SMTP_PORT` is converted to an integer and missing or malformed values raise `ConfigError`. The repository README shows the Gmail-oriented example and notes that the password should be an app password.

## Contacts

`src/neocomposer/contacts_manager.py` reads `contacts.json` from the same config directory. The JSON shape is expected to include a `contacts` list, and each contact is converted to `Contact(name, email)`. Contacts are displayed and selected with 1-based indexes.

Relevant uses:

- `main.py --list-contacts`
- `main.py --contact-index`
- `interactive_io.prompt_recipient()`

## Templates

`src/neocomposer/templates_manager.py` discovers templates in `~/.config/neocomposer/templates/` with `.html`, `.txt`, or `.md` extensions. Templates can be referenced by filename, stem, or direct path.

Template parsing rules:

- Optional YAML-like frontmatter is supported only for simple `key: value` lines.
- The `subject` frontmatter field becomes the template subject.
- Variables use `{{name}}` placeholders in the subject or body.
- Rendering fails if required variables are missing or the template name is ambiguous.

In interactive mode, template variables can be prefilled before the body is edited in Neovim. In programmatic mode, CLI `--subject` and `--body` values override or seed template variables where present.

## Signature and attachments

`mail_composer.py` appends the package-local `signature.html` file when it exists. Attachments are added as MIME base parts, and missing attachment files produce a warning in the compose flow rather than a hard crash.

## Source references

- `src/neocomposer/config_manager.py`
- `src/neocomposer/contacts_manager.py`
- `src/neocomposer/contact.py`
- `src/neocomposer/templates_manager.py`
- `src/neocomposer/mail_composer.py`
- `src/neocomposer/paths.py`
- `README.md`
