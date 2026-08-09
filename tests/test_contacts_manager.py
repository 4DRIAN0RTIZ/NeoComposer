import json

import pytest

from neocomposer.contact import Contact
from neocomposer.contacts_manager import ContactsManager
from neocomposer.exceptions import ContactsError


def write_contacts(path, payload):
    path.write_text(json.dumps(payload))


def test_load_contacts_missing_file(tmp_path):
    manager = ContactsManager(str(tmp_path / "missing.json"))
    with pytest.raises(ContactsError, match="Contacts file not found"):
        manager.load_contacts()


def test_load_contacts_invalid_json(tmp_path):
    contacts_file = tmp_path / "contacts.json"
    contacts_file.write_text("{not valid json")

    manager = ContactsManager(str(contacts_file))
    with pytest.raises(ContactsError, match="Invalid JSON"):
        manager.load_contacts()


def test_load_contacts_not_a_list(tmp_path):
    contacts_file = tmp_path / "contacts.json"
    write_contacts(contacts_file, {"contacts": "not-a-list"})

    manager = ContactsManager(str(contacts_file))
    with pytest.raises(ContactsError, match="must be a list"):
        manager.load_contacts()


def test_load_contacts_returns_contact_objects(tmp_path):
    contacts_file = tmp_path / "contacts.json"
    write_contacts(
        contacts_file,
        {"contacts": [{"name": "Ada", "email": "ada@example.com"}]},
    )

    manager = ContactsManager(str(contacts_file))
    contacts = manager.load_contacts()

    assert contacts == [Contact("Ada", "ada@example.com")]


def test_load_contacts_defaults_missing_key(tmp_path):
    contacts_file = tmp_path / "contacts.json"
    write_contacts(contacts_file, {})

    manager = ContactsManager(str(contacts_file))
    assert manager.load_contacts() == []


def test_get_contacts_caches_after_load(tmp_path):
    contacts_file = tmp_path / "contacts.json"
    write_contacts(
        contacts_file,
        {"contacts": [{"name": "Ada", "email": "ada@example.com"}]},
    )

    manager = ContactsManager(str(contacts_file))
    first = manager.get_contacts()
    contacts_file.write_text(json.dumps({"contacts": []}))
    second = manager.get_contacts()

    assert first == second


def test_get_contact_by_index_valid(tmp_path):
    contacts_file = tmp_path / "contacts.json"
    write_contacts(
        contacts_file,
        {
            "contacts": [
                {"name": "Ada", "email": "ada@example.com"},
                {"name": "Bob", "email": "bob@example.com"},
            ]
        },
    )

    manager = ContactsManager(str(contacts_file))
    assert manager.get_contact_by_index(2) == Contact("Bob", "bob@example.com")


@pytest.mark.parametrize("index", [0, -1, 3])
def test_get_contact_by_index_out_of_range(tmp_path, index):
    contacts_file = tmp_path / "contacts.json"
    write_contacts(
        contacts_file,
        {"contacts": [{"name": "Ada", "email": "ada@example.com"}]},
    )

    manager = ContactsManager(str(contacts_file))
    with pytest.raises(ContactsError, match="Invalid index"):
        manager.get_contact_by_index(index)


def test_format_contacts(tmp_path):
    contacts_file = tmp_path / "contacts.json"
    write_contacts(
        contacts_file,
        {
            "contacts": [
                {"name": "Ada", "email": "ada@example.com"},
                {"name": "Bob", "email": "bob@example.com"},
            ]
        },
    )

    manager = ContactsManager(str(contacts_file))
    formatted = manager.format_contacts()

    assert formatted == (
        "Contacts:\n1. Ada (ada@example.com)\n2. Bob (bob@example.com)"
    )
