import os


def get_config_dir() -> str:
    """Path to NeoComposer's configuration directory"""
    return os.path.expanduser(f"~{os.getlogin()}/.config/neocomposer")


def get_env_path() -> str:
    """Path to the .env configuration file"""
    return os.path.join(get_config_dir(), ".env")


def get_contacts_path() -> str:
    """Path to the contacts.json file"""
    return os.path.join(get_config_dir(), "contacts.json")


def get_contacts_script_path() -> str:
    """Path to the contacts.sh script"""
    return os.path.join(get_config_dir(), "contacts.sh")
