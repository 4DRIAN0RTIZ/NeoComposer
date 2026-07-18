import os
from dotenv import load_dotenv
from typing import Optional

from . import paths
from .exceptions import ConfigError


class ConfigManager:
    """Handles loading and validating configuration from .env"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: Path to the .env file. If not specified, uses the default path
        """
        self.config_path = config_path or paths.get_env_path()

    def load(self) -> dict:
        """
        Loads the configuration from the .env file

        Returns:
            dict with SMTP and sender configuration

        Raises:
            ConfigError: If the .env file does not exist or required variables are missing
        """
        if not os.path.exists(self.config_path):
            raise ConfigError(
                f"Configuration file not found: {self.config_path}"
            )

        load_dotenv(self.config_path)

        config = {
            "smtp_server": os.getenv("SMTP_SERVER"),
            "smtp_port": os.getenv("SMTP_PORT"),
            "sender_email": os.getenv("SENDER_EMAIL"),
            "sender_password": os.getenv("SENDER_PASSWORD"),
            "sender_name": os.getenv("SENDER_NAME"),
        }

        required_fields = [
            "smtp_server",
            "smtp_port",
            "sender_email",
            "sender_password",
            "sender_name",
        ]
        missing = [field for field in required_fields if not config[field]]

        if missing:
            raise ConfigError(f"Missing environment variables: {', '.join(missing)}")

        # Convert port to integer
        try:
            config["smtp_port"] = int(config["smtp_port"])
        except (ValueError, TypeError):
            raise ConfigError("SMTP_PORT must be an integer")

        return config

    def get_config_path(self) -> str:
        """Returns the path of the configuration file"""
        return self.config_path
