import json
import os
from typing import List, Dict, Any


class AgendaManager:
    """Gestiona la carga y operaciones con la agenda de contactos"""

    def __init__(self, agenda_path: str):
        """
        Args:
            agenda_path: Ruta completa al archivo agenda.json
        """
        self.agenda_path = agenda_path
        self._contacts = None

    def load_agenda(self) -> List[Dict[str, Any]]:
        """
        Carga la agenda de contactos desde archivo JSON

        Returns:
            Lista de diccionarios con contactos {nombre, correo}

        Raises:
            FileNotFoundError: Si el archivo no existe
            json.JSONDecodeError: Si el JSON es inválido
        """
        try:
            with open(self.agenda_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                contacts = data.get("contactos", [])

            if not isinstance(contacts, list):
                raise ValueError(
                    "Formato de agenda inválido: 'contactos' debe ser una lista"
                )

            self._contacts = contacts
            return contacts

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Archivo de agenda no encontrado: {self.agenda_path}"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido en {self.agenda_path}: {str(e)}")

    def get_contacts(self) -> List[Dict[str, Any]]:
        """Retorna la lista de contactos cargada (cached)"""
        if self._contacts is None:
            return self.load_agenda()
        return self._contacts

    def get_contact_by_index(self, index: int) -> Dict[str, Any]:
        """
        Obtiene un contacto por su índice (1-indexed, como muestra la UI)

        Raises:
            ValueError: Si el índice es inválido
        """
        contacts = self.get_contacts()

        if not 1 <= index <= len(contacts):
            raise ValueError(f"Índice inválido. Debe ser entre 1 y {len(contacts)}")

        return contacts[index - 1]

    def display_contacts(self) -> None:
        """Muestra los contactos en formato legible para consola"""
        contacts = self.get_contacts()

        print("Contactos en la agenda:")
        for i, contacto in enumerate(contacts, 1):
            nombre = contacto.get("nombre", "Sin nombre")
            correo = contacto.get("correo", "Sin correo")
            print(f"{i}. {nombre} ({correo})")
