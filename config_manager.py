import os
from dotenv import load_dotenv
from typing import Optional


class ConfigManager:
    """Gestiona la carga y validación de configuración desde .env"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: Ruta al archivo .env. Si no se especifica, usa el path por defecto
        """
        self.username = os.getlogin()
        self.config_path = config_path or os.path.expanduser(
            f"~{self.username}/.config/neocomposer/.env"
        )

    def load(self) -> dict:
        """
        Carga la configuración desde el archivo .env

        Returns:
            dict con las configuraciones SMTP y remitente

        Raises:
            FileNotFoundError: Si el archivo .env no existe
            ValueError: Si faltan variables obligatorias
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Archivo de configuración no encontrado: {self.config_path}"
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
        ]
        missing = [field for field in required_fields if not config[field]]

        if missing:
            raise ValueError(f"Variables de entorno faltantes: {', '.join(missing)}")

        # Convertir puerto a entero
        try:
            config["smtp_port"] = int(config["smtp_port"])
        except (ValueError, TypeError):
            raise ValueError("SMTP_PORT debe ser un número entero")

        return config

    def get_config_path(self) -> str:
        """Retorna la ruta del archivo de configuración"""
        return self.config_path
