# Operations and setup

NeoComposer is intended to be used from a user config directory, not from project checkout state. The main operational tasks are installation, local configuration, and verifying that external tools are present.

## Installation and setup

The README describes a script-based installation flow:

```bash
git clone https://github.com/4DRIAN0RTIZ/NeoComposer.git
cd NeoComposer
sudo chmod +x install_neocomposer.sh
./install_neocomposer.sh
```

After installation, users are expected to edit `~/.config/neocomposer/.env` with SMTP credentials. The code also expects the contacts file and template directory to live under that same config directory.

## Runtime dependencies

The project assumes these external tools exist when using the interactive flow:

- `nvim` for body editing
- `yazi` for attachment selection
- SMTP access with STARTTLS

The package dependency list in `pyproject.toml` is intentionally small: only `python-dotenv` is required at runtime, with `pytest` and `pytest-mock` in the optional dev set.

## Operational watch-outs

- `paths.get_config_dir()` derives the config path from the current user home directory. That means code should not assume the repo checkout contains config files.
- Missing `.env`, contacts, templates, or attachments surface as explicit errors or warnings.
- Because the mail sender always uses STARTTLS and authentication, incorrect SMTP settings fail before send.

## Source references

- `README.md`
- `pyproject.toml`
- `src/neocomposer/paths.py`
- `src/neocomposer/config_manager.py`
- `src/neocomposer/interactive_io.py`
- `src/neocomposer/mail_sender.py`
