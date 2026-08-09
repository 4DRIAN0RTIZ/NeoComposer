# Testing guidance

NeoComposer has focused pytest coverage around parser behavior, template handling, interactive helpers, and the email orchestration path. The main test entry points live in `tests/`.

## What is covered

- `tests/test_main.py` checks CLI parsing, utility flags, programmatic dispatch, body-file handling, and template variable parsing.
- Other tests cover config loading, contacts, email composition/sending, interactive I/O, paths, and templates.

## What to run

The repository uses pytest, configured via `pyproject.toml` to look in the `tests` directory. When changing CLI behavior or orchestration, run at least the targeted tests for `test_main.py` and any impacted domain tests.

## Change-oriented guidance

- Update parser tests when adding or renaming CLI flags.
- Update template tests when changing frontmatter, variable interpolation, or path resolution.
- Update config and contacts tests when changing file formats or required fields.
- Update email tests when changing MIME composition, attachment handling, or SMTP behavior.

## Source references

- `tests/test_main.py`
- `tests/test_templates_manager.py`
- `tests/test_config_manager.py`
- `tests/test_contacts_manager.py`
- `tests/test_email_client.py`
- `pyproject.toml`
