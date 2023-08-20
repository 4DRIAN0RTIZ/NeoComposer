import json
import sys
import os
from dotenv import load_dotenv
import traceback
from email_functions import smtp_login, print_loading_animation, open_explorer, open_neovim
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailClient:
    def __init__(self):
        self.username = os.getlogin()
        self.agenda_path = f"/home/{self.username}/.config/neocomposer/agenda.json"
        self.script_path = f"/home/{self.username}/.config/neocomposer/agenda.sh"

    def load_configuration(self):
        # Carga la configuración desde el archivo .env
        env_path = os.path.expanduser(f"~{self.username}/.config/neocomposer/.env")
        load_dotenv(env_path)

    def load_agenda(self):
        # Carga la agenda de contactos desde el archivo "agenda.json"
        with open(self.agenda_path, "r") as agenda_file:
            agenda = json.load(agenda_file)
        return agenda

    def smtp_login(self, server, port, sender_email, sender_password):
        return smtp_login(server, port, sender_email, sender_password)

    def print_loading_animation(self, seconds, char_list):
        print_loading_animation(seconds, char_list)

    def open_explorer(self):
        return open_explorer()

    def open_neovim(self):
        return open_neovim()

    def run(self):
        # Implementa el flujo principal de la aplicación aquí
        try:
            self.load_configuration()
            agenda = self.load_agenda()

            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT'))
            sender_email = os.getenv('SENDER_EMAIL')
            sender_password = os.getenv('SENDER_PASSWORD')
            sender_name = os.getenv('SENDER_NAME')

            os.system("clear")

            print("Seleccione una opción:")
            print("1. Enviar a un destinatario de uso único")
            print("2. Elegir un destinatario de la agenda")

            opcion = input("Opción: ")

            if opcion == "1":
                destinatario = input("Correo destinatario: ")
            elif opcion == "2":
                print("Contactos en la agenda:")
                for i, contacto in enumerate(agenda["contactos"], 1):
                    print(f"{i}. {contacto['nombre']} ({contacto['correo']})")

                while True:
                    try:
                        seleccion = int(input("Número de contacto: "))
                        if 1 <= seleccion <= len(agenda["contactos"]):
                            destinatario = agenda["contactos"][seleccion - 1]["correo"]
                            break
                        else:
                            print("Número de contacto no válido. Por favor, elige un número válido.")
                    except ValueError:
                        print("Debes ingresar un número válido.")
            else:
                print("Opción no válida. Saliendo del programa.")
                sys.exit(1)

            asunto = input("Asunto: ")

            if os.path.exists('signature.html'):
                with open('signature.html', 'r') as f:
                    firma = f.read()
            else:
                firma = ''

            cuerpo = self.open_neovim()
            cuerpo_html = cuerpo.replace('\n', '<br>')

            adjuntar = input("¿Deseas adjuntar un archivo? (S/N): ")

            smtp = self.smtp_login(smtp_server, smtp_port, sender_email, sender_password)
            if smtp:
                try:
                    mensaje = MIMEMultipart()
                    cuerpo_html += firma
                    parte_texto = MIMEText(cuerpo_html, "html")
                    mensaje.attach(parte_texto)

                    while adjuntar.lower() == "s":
                        archivo = self.open_explorer()
                        if archivo:
                            with open(archivo, "rb") as attachment:
                                adjunto = MIMEBase("application", "octet-stream")
                                adjunto.set_payload(attachment.read())
                                encoders.encode_base64(adjunto)
                                adjunto.add_header(
                                    "Content-Disposition", f"attachment; filename= {os.path.basename(archivo)}"
                                )
                                mensaje.attach(adjunto)

                        adjuntar = input("¿Deseas adjuntar otro archivo? (S/N): ")

                    mensaje["Subject"] = asunto
                    mensaje["From"] = f"{sender_name} <{sender_email}>"
                    mensaje["To"] = destinatario

                    self.print_loading_animation(1, ['|', '/', '-', '\\'])
                    smtp.sendmail(sender_email, destinatario, mensaje.as_string())

                    if smtp.noop()[0] == 250:
                        print("\rCorreo enviado exitosamente")
                    else:
                        print("\rHa ocurrido un error")
                except Exception as e:
                    print(f"Error al enviar el correo: {str(e)}")
                    traceback.print_exc()
                finally:
                    smtp.quit()
            else:
                print("No se pudo establecer una conexión SMTP válida.")

            os.remove("emailtemp.txt")
            if os.path.exists("temp.txt"):
                os.remove("temp.txt")
        except Exception as e:
            print(f"Error en la aplicación: {str(e)}")
            traceback.print_exc()
