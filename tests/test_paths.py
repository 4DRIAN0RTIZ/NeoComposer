import os

import pytest

from neocomposer import paths


@pytest.fixture(autouse=True)
def fixed_login(monkeypatch):
    monkeypatch.setattr(os, "getlogin", lambda: "testuser")


def test_get_config_dir():
    assert paths.get_config_dir() == os.path.expanduser("~testuser/.config/neocomposer")


def test_get_env_path():
    assert paths.get_env_path() == os.path.join(paths.get_config_dir(), ".env")


def test_get_contacts_path():
    assert paths.get_contacts_path() == os.path.join(paths.get_config_dir(), "contacts.json")


def test_get_contacts_script_path():
    assert paths.get_contacts_script_path() == os.path.join(
        paths.get_config_dir(), "contacts.sh"
    )


def test_get_templates_dir():
    assert paths.get_templates_dir() == os.path.join(paths.get_config_dir(), "templates")
