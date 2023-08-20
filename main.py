#!/usr/bin/env python3

import os
import argparse
from email_client import EmailClient

def main():
    parser = argparse.ArgumentParser(description="Neocomposer - Send emails from terminal")
    
    parser.add_argument("-a", "--agenda", action="store_true", help="Open the neocomposer agenda")
    
    args = parser.parse_args()
    
    if args.agenda:
        try:
            # Ejecuta script de agenda
            script_path = f"/home/{os.getlogin()}/.config/neocomposer/agenda.sh"
            os.system(script_path)
            return

        except Exception as e:
            print("Error al ejecutar agenda: ", str(e))
            return
    
    try:
        email_client = EmailClient()
        email_client.run()
    except KeyboardInterrupt:
        print("\nFinalizando neocomposer...")

if __name__ == "__main__":
    main()
