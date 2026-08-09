# NeoComposer OpenWiki

NeoComposer is a terminal-first email client written in Python. It supports an interactive flow with Neovim and Yazi plus a programmatic CLI for scripts and automation.

Start here if you are new to the repo.

## What this project does

- Loads SMTP credentials from a per-user `.env` file under `~/.config/neocomposer/.env`.
- Builds MIME email messages with an optional HTML signature and attachments.
- Sends mail over SMTP with STARTTLS.
- Lets users manage a JSON contacts list and reusable email templates.
- Supports both interactive composition and programmatic sending from the CLI.

## Repository map

- [Architecture overview](architecture/overview.md)
- [CLI and workflows](workflows/cli.md)
- [Configuration, contacts, and templates](domain/data-and-templates.md)
- [Operations and setup](operations/setup.md)
- [Testing guidance](testing.md)

## Source anchors

- CLI entrypoint: `src/neocomposer/main.py`
- Orchestrator: `src/neocomposer/email_client.py`
- Configuration loader: `src/neocomposer/config_manager.py`
- Contacts manager: `src/neocomposer/contacts_manager.py`
- Templates manager: `src/neocomposer/templates_manager.py`
- Composer and sender: `src/neocomposer/mail_composer.py`, `src/neocomposer/mail_sender.py`
- Path helpers: `src/neocomposer/paths.py`

## How to use these notes

Read the CLI workflow page first when changing user-facing behavior. Read the domain pages when changing config, contacts, or templates. Read testing guidance before editing behavior in `main.py` or `email_client.py`.
