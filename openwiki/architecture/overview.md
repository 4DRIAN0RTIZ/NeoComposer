# Architecture overview

NeoComposer is a small Python CLI with one main orchestration path and a few focused helper modules. The code is organized around the steps of composing and sending email rather than around transport abstractions or a web stack.

## Main flow

1. `src/neocomposer/main.py` parses CLI flags and decides whether the run is interactive or programmatic.
2. `src/neocomposer/email_client.py` orchestrates config loading, recipient selection, template rendering, message composition, attachment handling, and SMTP sending.
3. `src/neocomposer/mail_composer.py` builds the MIME message and applies the HTML signature.
4. `src/neocomposer/mail_sender.py` opens the SMTP connection, starts TLS, logs in, and sends the message.

## Supporting modules

- `src/neocomposer/config_manager.py` loads `.env` values with `python-dotenv` and validates required SMTP settings.
- `src/neocomposer/contacts_manager.py` reads `contacts.json` and formats indexed contact output.
- `src/neocomposer/templates_manager.py` discovers, parses, and renders reusable templates.
- `src/neocomposer/interactive_io.py` contains the terminal prompts, Neovim/Yazi integrations, and send animation.
- `src/neocomposer/paths.py` centralizes config paths under the user config directory.
- `src/neocomposer/exceptions.py` defines the domain error hierarchy used to distinguish configuration, contacts, compose, send, and template failures.

## Design notes

- The project keeps the CLI thin so tests can focus on parsing and dispatch.
- Template rendering happens before interactive composition so template defaults can seed the editor.
- The code treats missing contacts/templates/config as user-facing errors, not silent fallbacks.
- `MailComposer` keeps the signature loading local to the package so packaging does not depend on the current working directory.

## Source references

- `src/neocomposer/main.py`
- `src/neocomposer/email_client.py`
- `src/neocomposer/mail_composer.py`
- `src/neocomposer/mail_sender.py`
- `src/neocomposer/config_manager.py`
- `src/neocomposer/templates_manager.py`
- `src/neocomposer/interactive_io.py`
