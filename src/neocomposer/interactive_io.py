import os
import tempfile
import time
from typing import List

from .contacts_manager import ContactsManager
from .exceptions import ContactsError


def _run_editor_and_capture(shell_cmd: str, mode: str = "w+", strip_result: bool = False) -> str:
    """Creates a temp file, opens it with the given command, and captures its content"""
    with tempfile.NamedTemporaryFile(mode=mode, delete=False, suffix=".txt") as f:
        temp_path = f.name

    try:
        os.system(shell_cmd.format(path=temp_path))
        with open(temp_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content.strip() if strip_result else content
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def select_file_with_yazi() -> str:
    """Uses yazi to select a file"""
    return _run_editor_and_capture("yazi --chooser-file={path}", mode="w", strip_result=True)


def compose_body_with_neovim() -> str:
    """Creates the email body using neovim"""
    return _run_editor_and_capture("nvim {path}", mode="w+")


def prompt_recipient(contacts: ContactsManager) -> str:
    """Asks for the recipient interactively (manual or from contacts)"""
    print("Select an option:")
    print("1. Send to a one-time recipient")
    print("2. Choose a recipient from the contacts list")

    option = input("Option: ").strip()

    if option == "1":
        return input("Recipient email: ").strip()

    if option == "2":
        print(contacts.format_contacts())

        while True:
            try:
                selection = int(input("Contact number: "))
                contact = contacts.get_contact_by_index(selection)
                return contact.email
            except (ValueError, ContactsError) as e:
                print(f"Invalid selection: {e}")

    raise ContactsError("Invalid option.")


def prompt_attachments() -> List[str]:
    """Asks for attachments interactively using yazi"""
    attachments = []

    while True:
        attach = input("Do you want to attach a file? (y/n): ").strip().lower()
        if attach != "y":
            break

        try:
            file_path = select_file_with_yazi()
            if file_path:
                attachments.append(file_path)
        except Exception as e:
            print(f"Error selecting file: {e}")

    return attachments


def clear_screen() -> None:
    os.system("clear")


def show_sending_animation(seconds: float, char_list: List[str]) -> None:
    """
    Shows a loading animation while sending

    Args:
        seconds: Animation duration
        char_list: List of characters to rotate (e.g.: ['|', '/', '-', '\\'])
    """
    for _ in range(int(seconds * 10)):  # 10 iterations per second
        for char in char_list:
            print(f"\rSending email... {char}", end="")
            time.sleep(0.1)
    print()  # New line when done


def print_send_result(success: bool, programmatic: bool = False) -> None:
    """Prints the send result depending on the mode"""
    if success:
        suffix = " (programmatic mode)" if programmatic else ""
        print(f"✓ Email sent successfully{suffix}")
    elif programmatic:
        print("✗ Error in programmatic send")
    else:
        print("✗ An error occurred")
