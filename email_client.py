import os
import sys
from typing import Optional, List
from config_manager import ConfigManager
from agenda_manager import AgendaManager
from mail_composer import MailComposer
from mail_sender import MailSender


class EmailClient:
    """Orquestador principal con modos interactivo y programático"""

    def __init__(
        self,
        recipient: Optional[str] = None,
        subject: Optional[str] = None,
        body: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        use_agenda: Optional[int] = None,
    ):
        """
        Args:
            recipient: Email destinatario (modo programático)
            subject: Asunto (modo programático)
            body: Cuerpo del mensaje (modo programático)
            attachments: Lista de archivos a adjuntar (modo programático)
            use_agenda: Índice del contacto en agenda (1-indexed, modo programático)
        """
        self.username = os.getlogin()
        self.config_path = os.path.expanduser(
            f"~{self.username}/.config/neocomposer/.env"
        )
        self.agenda_path = os.path.expanduser(
            f"~{self.username}/.config/neocomposer/agenda.json"
        )

        # Modo programático
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.use_agenda = use_agenda
        self._is_programmatic = any([recipient, subject, body, attachments, use_agenda])

    def _get_recipient_interactive(self) -> str:
        """Versión interactiva de obtención de destinatario"""
        print("Seleccione una opción:")
        print("1. Enviar a un destinatario de uso único")
        print("2. Elegir un destinatario de la agenda")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            return input("Correo destinatario: ").strip()

        if opcion == "2":
            agenda = AgendaManager(self.agenda_path)
            agenda.display_contacts()

            while True:
                try:
                    seleccion = int(input("Número de contacto: "))
                    contact = agenda.get_contact_by_index(seleccion)
                    return contact["correo"]
                except (ValueError, KeyError) as e:
                    print(f"Selección inválida: {e}")

        print("Opción no válida.")
        sys.exit(1)

    def _get_attachments_interactive(self) -> list[str]:
        """Versión interactiva de obtención de adjuntos"""
        attachments = []

        while True:
            adjuntar = input("¿Deseas adjuntar un archivo? (S/N): ").strip().lower()
            if adjuntar != "s":
                break

            try:
                archivo = self._select_file_with_yazi()
                if archivo:
                    attachments.append(archivo)
            except Exception as e:
                print(f"Error seleccionando archivo: {e}")

        return attachments

    def _select_file_with_yazi(self) -> str:
        """Usa yazi para seleccionar archivo"""
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            os.system(f"yazi --chooser-file={temp_path}")
            with open(temp_path, "r") as f:
                return f.read().strip()
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _compose_body_with_neovim(self) -> str:
        """Crea cuerpo del email usando neovim"""
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as f:
            temp_path = f.name

        try:
            os.system(f"nvim {temp_path}")
            with open(temp_path, "r", encoding="utf-8") as f:
                return f.read()
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
    ) -> bool:
        """
        Envío programático de email

        Args:
            recipient: Email destinatario
            subject: Asunto del mensaje
            body: Cuerpo del mensaje (puede ser plaintext)
            attachments: Lista opcional de rutas de archivos

        Returns:
            bool: True si el envío fue exitoso

        Raises:
            Exception: Si hay error en configuración, composición o envío
        """
        # 1. Cargar configuración
        config_manager = ConfigManager()
        config = config_manager.load()

        # 2. Componer mensaje
        composer = MailComposer()
        mensaje = composer.compose(
            subject=subject,
            sender_name=config["sender_name"],
            sender_email=config["sender_email"],
            recipient=recipient,
            body_html=body.replace("\n", "<br>") if body else "",
        )

        # 3. Adjuntar archivos
        if attachments:
            for archivo in attachments:
                if os.path.exists(archivo):
                    composer.add_attachment(mensaje, archivo)
                else:
                    print(f"Advertencia: Archivo no encontrado {archivo}")

        # 4. Enviar
        sender = MailSender(
            smtp_server=config["smtp_server"],
            smtp_port=config["smtp_port"],
            sender_email=config["sender_email"],
            sender_password=config["sender_password"],
        )

        return sender.send(mensaje, recipient)

    def run_interactive(self) -> None:
        """Ejecuta el flujo interactivo"""
        os.system("clear")

        # 1. Cargar configuración
        config_manager = ConfigManager()
        config = config_manager.load()

        # 2. Recopilar datos interactivamente
        destinatario = self._get_recipient_interactive()
        asunto = input("Asunto: ").strip()
        cuerpo = self._compose_body_with_neovim()
        adjuntos = self._get_attachments_interactive()

        # 3. Componer y enviar
        composer = MailComposer()
        mensaje = composer.compose(
            subject=asunto,
            sender_name=config["sender_name"],
            sender_email=config["sender_email"],
            recipient=destinatario,
            body_html=cuerpo.replace("\n", "<br>"),
        )

        for archivo in adjuntos:
            if os.path.exists(archivo):
                composer.add_attachment(mensaje, archivo)

        sender = MailSender(
            smtp_server=config["smtp_server"],
            smtp_port=config["smtp_port"],
            sender_email=config["sender_email"],
            sender_password=config["sender_password"],
        )

        sender.print_loading_animation(1, ["|", "/", "-", "\\"])
        success = sender.send(mensaje, destinatario)

        if success:
            print("✓ Correo enviado exitosamente")
        else:
            print("✗ Ha ocurrido un error")

    def run(self) -> None:
        """Detecta modo y ejecuta el flujo correspondiente"""
        try:
            if self._is_programmatic:
                # Modo programático
                recipient = self.recipient

                if self.use_agenda:
                    agenda = AgendaManager(self.agenda_path)
                    contact = agenda.get_contact_by_index(self.use_agenda)
                    recipient = contact["correo"]

                success = self.send_email(
                    recipient=recipient,
                    subject=self.subject or "(Sin asunto)",
                    body=self.body or "",
                    attachments=self.attachments,
                )

                if success:
                    print("✓ Correo enviado exitosamente (modo programático)")
                else:
                    print("✗ Error en envío programático")
                    sys.exit(1)

            else:
                # Modo interactivo
                self.run_interactive()

        except Exception as e:
            print(f"\nError crítico: {str(e)}")
            import traceback

            traceback.print_exc()
            sys.exit(1)
