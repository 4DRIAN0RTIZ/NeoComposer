# CLI and workflows

NeoComposer exposes a single `neocomposer` command with utility flags, an interactive mode, and a programmatic mode. The CLI surface is defined in `src/neocomposer/main.py` and executed by `EmailClient` in `src/neocomposer/email_client.py`.

## Execution modes

### Utility flags

These short-circuit before mail composition:

- `--open-contacts` / `--contacts` runs the contacts shell script from the config directory.
- `--list-contacts` prints the formatted JSON contacts list.
- `--list-templates` prints templates discovered in the templates directory.

### Programmatic mode

Programmatic mode is used when non-interactive flags are supplied. It supports:

- `--recipient` or `--contact-index` to choose a recipient.
- `--subject`, `--body`, or `--body-file` for content.
- `--attachments` for one or more files.
- `--template` plus repeatable `--template-var KEY=VALUE` for rendering reusable templates.

The CLI validates template variables before constructing the client, and it rejects programmatic runs that do not include a recipient source.

### Interactive mode

Interactive mode is the default when no programmatic arguments are present. The flow in `EmailClient.run_interactive()` is:

1. Clear the terminal.
2. Load config.
3. Prompt for recipient, either manual or from contacts.
4. Optionally select a reusable template.
5. Prompt for missing template variables.
6. Collect the subject and open Neovim for body editing.
7. Prompt for optional attachments via Yazi.
8. Build and send the message.

## Change points and cautions

- Update `main.py` when adding flags or changing mode detection.
- Update `email_client.py` when changing how CLI data becomes a sent email.
- Keep tests in `tests/test_main.py` in sync with any parser or dispatch changes.
- Be careful with `--contact-index`: the rest of the code treats contacts as 1-indexed, matching the UI.

## Source references

- `src/neocomposer/main.py`
- `src/neocomposer/email_client.py`
- `src/neocomposer/interactive_io.py`
