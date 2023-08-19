#!/usr/bin/env python3

"""
Este script envía correos electrónicos con adjuntos a través de SMTP.

Dependencias: Ranger, Neovim y Dotenv

El script carga la configuración desde un archivo .env
y permite al usuario especificar el destinatario, el asunto y el
cuerpo del correo. 
Brinda la opción de adjuntar uno o varios archivos al correo.
Toma el archivo "signature.html" de la carpeta raíz y lo toma como firma.

Author: 4DRIAN0RTIZ
Version: 1.0.0
Date: 10-08-2023
License: Free Use
"""

import json
import sys
import time
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Obtener el nombre de usuario actual
username = os.getlogin()
# Ruta del archivo "agenda.json"
agenda_path = f"/home/{username}/.config/neocomposer/agenda.json"
# Construir la ruta del archivo "agenda.sh"
script_path = f"/home/{username}/.config/neocomposer/agenda.sh"
# Verifica si se ha pasado algún argumento
if "-a" in sys.argv:
    try:
        # Ejecutar el script "agenda.sh" si se proporciona la flag "-a"
        os.system(script_path)
        sys.exit(1)
    except Exception as e:
        print("Error al ejecutar agenda.sh:", str(e))
        sys.exit(1)


def print_loading_animation(seconds,char_list):
    for _ in range(int(seconds + 10)):
        for char in char_list:
            print(f"\rEnviando correo... {char}", end="")
            time.sleep(0.1)


def open_explorer():
    os.system("ranger --choosefile=temp.txt")
    with open("temp.txt", "r") as f:
        return f.read()


def open_neovim():
    filename = "emailtemp.txt"
    os.system("nvim " + filename)
    with open(filename, "r") as f:
        return f.read()


# Carga la configuración desde el archivo .env
env_path = os.path.expanduser(
    f"~{username}/.config/neocomposer/.env")
load_dotenv(env_path)

# Carga la agenda de contactos desde el archivo "agenda.json"
with open(agenda_path, "r") as agenda_file:
    agenda = json.load(agenda_file)

# Obtiene los valores de configuración del archivo .env
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
sender_name = os.getenv('SENDER_NAME')

# Limpia la pantalla
os.system("clear")

print("Seleccione una opción:")
print("1. Enviar a un destinatario de uso único")
print("2. Elegir un destinatario de la agenda")

opcion = input("Opción: ")

if opcion == "1":
    # El usuario quiere ingresar un destinatario de uso único
    destinatario = input("Correo destinatario: ")
elif opcion == "2":
    # El usuario quiere seleccionar un destinatario de la agenda
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

# Verificar la existencia de signature.html

if os.path.exists('signature.html'):
    with open('signature.html', 'r') as f:
        firma = f.read()
else:
    firma = ''

cuerpo = open_neovim()

# Reemplaza los saltos de línea por etiquetas <br> en el cuerpo
cuerpo_html = cuerpo.replace('\n', '<br>')

adjuntar = input("¿Deseas adjuntar un archivo? (S/N): ")

# Crea la conexión SMTP
with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    smtp.starttls()
    smtp.login(sender_email, sender_password)

    # Construye el mensaje multipart
    mensaje = MIMEMultipart()

    # Crea las partes del mensaje (texto y HTML)
    cuerpo_html += firma
    parte_texto = MIMEText(cuerpo_html, "html")

    mensaje.attach(parte_texto)

    while adjuntar.lower() == "s":
        archivo = open_explorer()

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

    # Agrega las partes al mensaje
    mensaje["Subject"] = asunto
    mensaje["From"] = f"{sender_name} <{sender_email}>"
    mensaje["To"] = destinatario

    
    # Envía el mensaje
    print_loading_animation(1, ['|', '/', '-', '\\'])
    smtp.sendmail(sender_email, destinatario, mensaje.as_string())

    # Muestra mensaje de correo enviado en caso de ser exitoso
    if smtp.noop()[0] == 250:
        print("\rCorreo enviado exitosamente")
    else:
        print("\rHa ocurrido un error")

os.remove("emailtemp.txt")
# Si existe temp.txt lo elimina
if os.path.exists("temp.txt"):
    os.remove("temp.txt")

