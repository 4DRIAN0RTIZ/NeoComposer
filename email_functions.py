import smtplib
import time
import os

def smtp_login(server, port, sender_email, sender_password):
    try:
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        return smtp
    except smtplib.SMTPException as e:
        print(f"Error al autenticar SMTP: {str(e)}")
        return None

def print_loading_animation(seconds, char_list):
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

