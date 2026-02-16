import smtplib
import time
from email.mime.multipart import MIMEMultipart
from contextlib import contextmanager
from typing import Optional


class MailSender:
    """Maneja la conexión SMTP y el envío de mensajes"""

    def __init__(
        self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str
    ):
        """
        Args:
            smtp_server: Servidor SMTP
            smtp_port: Puerto SMTP
            sender_email: Email del remitente
            sender_password: Contraseña del remitente
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    @contextmanager
    def connect(self) -> smtplib.SMTP:
        """
        Context manager para conexiones SMTP seguras

        Yields:
            smtplib.SMTP: Conexión autenticada

        Raises:
            smtplib.SMTPException: Si falla la autenticación
        """
        smtp = None
        try:
            smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp.starttls()
            smtp.login(self.sender_email, self.sender_password)
            yield smtp
        except smtplib.SMTPException as e:
            raise ConnectionError(f"Error de autenticación SMTP: {str(e)}") from e
        finally:
            if smtp:
                try:
                    smtp.quit()
                except Exception:
                    pass

    def send(self, message: MIMEMultipart, recipient: str) -> bool:
        """
        Envía un mensaje a través de SMTP

        Args:
            message: Mensaje MIME compuesto
            recipient: Email del destinatario

        Returns:
            bool: True si fue exitoso

        Raises:
            Exception: Si el envío falla
        """
        with self.connect() as smtp:
            smtp.sendmail(self.sender_email, recipient, message.as_string())
            return smtp.noop()[0] == 250

    def print_loading_animation(self, seconds: float, char_list: list[str]) -> None:
        """
        Muestra animación de carga durante el envío

        Args:
            seconds: Duración de la animación
            char_list: Lista de caracteres a rotar (ej: ['|', '/', '-', '\\'])
        """
        for _ in range(int(seconds * 10)):  # 10 iteraciones por segundo
            for char in char_list:
                print(f"\rEnviando correo... {char}", end="")
                time.sleep(0.1)
        print()  # Nueva línea al finalizar
