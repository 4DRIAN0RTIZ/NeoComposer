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

import time
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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
username = os.getlogin()
env_path = os.path.expanduser(
    f"~{username}/.config/neocomposer/.env")
load_dotenv(env_path)

# Obtiene los valores de configuración del archivo .env
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
sender_name = os.getenv('SENDER_NAME')

destinatario = input("Correo destinatario: ")
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

