#!/usr/bin/env python3

import os
import sys
import argparse
from email_client import EmailClient


def main():
    parser = argparse.ArgumentParser(
        description="NeoComposer - Enviar emails desde terminal (interactivo o programático)"
    )

    # Modo interactivo (default)
    parser.add_argument(
        "--interactive",
        "-I",
        action="store_true",
        help="Modo interactivo (por defecto si no se pasan otros args)",
    )

    # Modo programático
    parser.add_argument(
        "--recipient",
        "-r",
        type=str,
        help="Email del destinatario (requerido en modo programático)",
    )

    parser.add_argument("--subject", "-s", type=str, help="Asunto del email")

    parser.add_argument(
        "--body", "-b", type=str, help="Cuerpo del mensaje (texto plano o HTML)"
    )

    parser.add_argument(
        "--body-file", "-f", type=str, help="Archivo con el cuerpo del mensaje"
    )

    parser.add_argument(
        "--attachments",
        "-a",
        type=str,
        nargs="+",
        help="Archivos a adjuntar (espacio separado)",
    )

    parser.add_argument(
        "--agenda-index",
        "-i",
        type=int,
        help="Índice del contacto en agenda (1-indexed, usa agenda en lugar de --recipient)",
    )

    # Utilidades
    parser.add_argument(
        "--list-contacts",
        "-l",
        action="store_true",
        help="Listar contactos de la agenda y salir",
    )

    parser.add_argument(
        "--open-agenda",
        "--agenda",
        action="store_true",
        help="Abrir la agenda de NeoComposer",
    )

    args = parser.parse_args()

    # Manejo de utilidades
    if args.open_agenda:
        try:
            script_path = os.path.expanduser(
                f"~{os.getlogin()}/.config/neocomposer/agenda.sh"
            )
            if os.path.exists(script_path):
                os.system(script_path)
            else:
                print(f"Error: Script de agenda no encontrado: {script_path}")
                sys.exit(1)
        except Exception as e:
            print(f"Error al ejecutar agenda: {str(e)}")
            sys.exit(1)
        return

    if args.list_contacts:
        try:
            from agenda_manager import AgendaManager

            username = os.getlogin()
            agenda_path = os.path.expanduser(
                f"~{username}/.config/neocomposer/agenda.json"
            )
            agenda = AgendaManager(agenda_path)
            agenda.display_contacts()
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
        return

    # Detectar modo programático
    is_programmatic = any(
        [
            args.recipient,
            args.subject,
            args.body,
            args.body_file,
            args.attachments,
            args.agenda_index,
        ]
    )

    if is_programmatic:
        # Modo programático
        if not args.recipient and not args.agenda_index:
            print("Error: Debes especificar --recipient o --agenda-index")
            sys.exit(1)

        # Leer body desde archivo si se especificó
        body = args.body
        if args.body_file:
            try:
                with open(args.body_file, "r", encoding="utf-8") as f:
                    body = f.read()
            except Exception as e:
                print(f"Error leyendo archivo de body: {str(e)}")
                sys.exit(1)

        try:
            client = EmailClient(
                recipient=args.recipient,
                subject=args.subject,
                body=body,
                attachments=args.attachments,
                use_agenda=args.agenda_index,
            )
            client.run()
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

    else:
        # Modo interactivo
        try:
            client = EmailClient()
            client.run_interactive()
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario")
            sys.exit(130)
        except Exception as e:
            print(f"\nError inesperado: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
