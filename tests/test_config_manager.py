import pytest

from neocomposer.config_manager import ConfigManager
from neocomposer.exceptions import ConfigError

ENV_KEYS = ["SMTP_SERVER", "SMTP_PORT", "SENDER_EMAIL", "SENDER_PASSWORD", "SENDER_NAME"]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for key in ENV_KEYS:
        monkeypatch.delenv(key, raising=False)


def write_env(path, **overrides):
    values = {
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
        "SENDER_EMAIL": "me@example.com",
        "SENDER_PASSWORD": "secret",
        "SENDER_NAME": "Me",
    }
    values.update(overrides)
    lines = [f"{key}={value}" for key, value in values.items() if value is not None]
    path.write_text("\n".join(lines))


def test_load_missing_file_raises(tmp_path):
    manager = ConfigManager(str(tmp_path / "missing.env"))
    with pytest.raises(ConfigError, match="Configuration file not found"):
        manager.load()


def test_load_valid_config(tmp_path):
    env_file = tmp_path / ".env"
    write_env(env_file)

    config = ConfigManager(str(env_file)).load()

    assert config == {
        "smtp_server": "smtp.example.com",
        "smtp_port": 587,
        "sender_email": "me@example.com",
        "sender_password": "secret",
        "sender_name": "Me",
    }


@pytest.mark.parametrize(
    "missing_key",
    ["SMTP_SERVER", "SMTP_PORT", "SENDER_EMAIL", "SENDER_PASSWORD", "SENDER_NAME"],
)
def test_load_missing_required_field_raises(tmp_path, missing_key):
    env_file = tmp_path / ".env"
    write_env(env_file, **{missing_key: None})

    manager = ConfigManager(str(env_file))
    with pytest.raises(ConfigError, match="Missing environment variables"):
        manager.load()


def test_load_invalid_port_raises(tmp_path):
    env_file = tmp_path / ".env"
    write_env(env_file, SMTP_PORT="not-a-number")

    manager = ConfigManager(str(env_file))
    with pytest.raises(ConfigError, match="SMTP_PORT must be an integer"):
        manager.load()


def test_get_config_path_defaults_to_env_path(monkeypatch):
    monkeypatch.setattr(
        "neocomposer.config_manager.paths.get_env_path", lambda: "/fake/.env"
    )
    manager = ConfigManager()
    assert manager.get_config_path() == "/fake/.env"


def test_get_config_path_returns_given_path():
    manager = ConfigManager("/custom/path/.env")
    assert manager.get_config_path() == "/custom/path/.env"
