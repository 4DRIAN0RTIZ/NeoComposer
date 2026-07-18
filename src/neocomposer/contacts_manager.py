import json
from typing import List

from .contact import Contact
from .exceptions import ContactsError


class ContactsManager:
    """Handles loading and operations on the contacts list"""

    def __init__(self, contacts_path: str):
        """
        Args:
            contacts_path: Full path to the contacts.json file
        """
        self.contacts_path = contacts_path
        self._contacts = None

    def load_contacts(self) -> List[Contact]:
        """
        Loads the contacts list from a JSON file

        Returns:
            List of Contact

        Raises:
            ContactsError: If the file does not exist or the JSON is invalid/malformed
        """
        try:
            with open(self.contacts_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_contacts = data.get("contacts", [])

            if not isinstance(raw_contacts, list):
                raise ContactsError(
                    "Invalid contacts format: 'contacts' must be a list"
                )

            contacts = [Contact.from_dict(c) for c in raw_contacts]
            self._contacts = contacts
            return contacts

        except FileNotFoundError:
            raise ContactsError(f"Contacts file not found: {self.contacts_path}")
        except json.JSONDecodeError as e:
            raise ContactsError(f"Invalid JSON in {self.contacts_path}: {str(e)}")

    def get_contacts(self) -> List[Contact]:
        """Returns the loaded contact list (cached)"""
        if self._contacts is None:
            return self.load_contacts()
        return self._contacts

    def get_contact_by_index(self, index: int) -> Contact:
        """
        Gets a contact by its index (1-indexed, as shown in the UI)

        Raises:
            ContactsError: If the index is invalid
        """
        contacts = self.get_contacts()

        if not 1 <= index <= len(contacts):
            raise ContactsError(f"Invalid index. Must be between 1 and {len(contacts)}")

        return contacts[index - 1]

    def format_contacts(self) -> str:
        """Formats the contacts as readable console text"""
        contacts = self.get_contacts()
        lines = ["Contacts:"]
        for i, contact in enumerate(contacts, 1):
            lines.append(f"{i}. {contact.name} ({contact.email})")
        return "\n".join(lines)
