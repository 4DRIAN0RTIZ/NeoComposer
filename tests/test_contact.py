from neocomposer.contact import Contact


def test_from_dict_full():
    contact = Contact.from_dict({"name": "Ada", "email": "ada@example.com"})
    assert contact.name == "Ada"
    assert contact.email == "ada@example.com"


def test_from_dict_missing_name_defaults():
    contact = Contact.from_dict({"email": "ada@example.com"})
    assert contact.name == "No name"
    assert contact.email == "ada@example.com"


def test_from_dict_missing_email_defaults():
    contact = Contact.from_dict({"name": "Ada"})
    assert contact.name == "Ada"
    assert contact.email == "No email"


def test_from_dict_empty():
    contact = Contact.from_dict({})
    assert contact.name == "No name"
    assert contact.email == "No email"


def test_contact_equality():
    assert Contact("Ada", "ada@example.com") == Contact("Ada", "ada@example.com")
