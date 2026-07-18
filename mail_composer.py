import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional


class MailComposer:
    """Compone mensajes MIME con cuerpo HTML, firma y adjuntos"""

    def __init__(self, signature_path: Optional[str] = None):
        """
        Args:
            signature_path: Ruta al archivo de firma HTML. Si no se especifica,
                usa signature.html junto al script (independiente del cwd).
        """
        self.signature_path = signature_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "signature.html"
        )
        self.signature_content = self._load_signature()

    def _load_signature(self) -> str:
        """Carga la firma HTML si existe"""
        try:
            if os.path.exists(self.signature_path):
                with open(self.signature_path, "r", encoding="utf-8") as f:
                    return f.read()
            return ""
        except Exception:
            return ""

    def compose(
        self,
        subject: str,
        sender_name: str,
        sender_email: str,
        recipient: str,
        body_html: str,
    ) -> MIMEMultipart:
        """
        Crea el mensaje MIME base con headers y cuerpo HTML

        Args:
            subject: Asunto del email
            sender_name: Nombre del remitente
            sender_email: Email del remitente
            recipient: Email del destinatario
            body_html: Cuerpo del mensaje en HTML
        """
        mensaje = MIMEMultipart()
        mensaje["Subject"] = subject
        mensaje["From"] = f"{sender_name} <{sender_email}>"
        mensaje["To"] = recipient

        # Adjuntar cuerpo HTML con firma
        full_body = body_html + self.signature_content
        parte_texto = MIMEText(full_body, "html")
        mensaje.attach(parte_texto)

        return mensaje

    def add_attachment(self, mensaje: MIMEMultipart, file_path: str) -> None:
        """
        Adjunta un archivo a un mensaje existente

        Args:
            mensaje: Mensaje MIME al que agregar el adjunto
            file_path: Ruta completa del archivo a adjuntar
        """
        try:
            with open(file_path, "rb") as attachment:
                adjunto = MIMEBase("application", "octet-stream")
                adjunto.set_payload(attachment.read())
                encoders.encode_base64(adjunto)
                adjunto.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(file_path)}",
                )
                mensaje.attach(adjunto)
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo adjunto no encontrado: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error adjuntando archivo {file_path}: {str(e)}")
