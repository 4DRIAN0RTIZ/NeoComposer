#!/bin/bash

# Script que funciona como la agenda de contactos de NeoComposer.
# Autor: 4DRIAN0RTIZ
# Fecha: 19/08/2023
# Descripción: Este script permite agregar, modificar y eliminar contactos de una agenda de contactos.

# Nombre del archivo que contiene la agenda
agenda_file="$HOME/.config/neocomposer/agenda.json"

# Función para agregar un nuevo contacto
function agregar_contacto() {
	clear
	echo "Ingrese el nombre o alias del contacto:"
	read nombre
	echo "Ingrese la dirección de correo electrónico del contacto:"
	read correo

	# Añadir el nuevo contacto al archivo JSON
	jq --arg nombre "$nombre" --arg correo "$correo" '.contactos += [{"nombre": $nombre, "correo": $correo}]' $agenda_file >tmp.$$.json && mv tmp.$$.json $agenda_file

	echo "Contacto agregado con éxito."
	read -p "Presione enter para continuar..."
}

# Función para modificar un contacto existente

function modificar_contacto() {
	clear
	echo "Ingrese el nombre o alias del contacto a modificar:"
	read nombre

	# Buscar el contacto en el archivo JSON
	contacto=$(jq --arg nombre "$nombre" '.contactos | map(select(.nombre == $nombre)) | .[0]' $agenda_file)

	# Si el contacto existe, mostrar sus datos y preguntar por los nuevos
	if [ -n "$contacto" ]; then
		echo "Datos actuales:"
		echo $contacto | jq

		# Preguntar qué dato se desea modificar
		echo "¿Qué dato desea modificar?"
		read -p "1) Nombre, 2) Correo, 3) Ambos: " opcion

		case "$opcion" in
		1)
			echo "Ingrese el nuevo nombre:"
			read nuevo_nombre
			jq --arg nombre "$nombre" --arg nuevo_nombre "$nuevo_nombre" \
				'.contactos |= map(if .nombre == $nombre then . + {"nombre": $nuevo_nombre} else . end)' \
				"$agenda_file" >temp.json && mv temp.json "$agenda_file"
			echo "Nombre modificado con éxito."
			;;
		2)
			echo "Ingrese el nuevo correo:"
			read nuevo_correo
			jq --arg nombre "$nombre" --arg nuevo_correo "$nuevo_correo" \
				'.contactos |= map(if .nombre == $nombre then . + {"correo": $nuevo_correo} else . end)' \
				"$agenda_file" >temp.json && mv temp.json "$agenda_file"
			echo "Correo modificado con éxito."
			;;
		3)
			echo "Ingrese el nuevo nombre:"
			read nuevo_nombre
			echo "Ingrese el nuevo correo:"
			read nuevo_correo
			jq --arg nombre "$nombre" --arg nuevo_nombre "$nuevo_nombre" --arg nuevo_correo "$nuevo_correo" \
				'.contactos |= map(if .nombre == $nombre then . + {"nombre": $nuevo_nombre, "correo": $nuevo_correo} else . end)' \
				"$agenda_file" >temp.json && mv temp.json "$agenda_file"
			echo "Nombre y correo modificados con éxito."
			;;
		*)
			echo "Opción no válida. No se realizó ninguna modificación."
			;;
		esac
	else
		echo "Contacto no encontrado."
	fi
	read-p "Presione enter para continuar..."
}

# Función para eliminar un contacto existente

function eliminar_contacto() {
	clear
	echo "Ingrese el nombre o alias del contacto a eliminar:"
	read nombre

	# Verificar si el contacto existe
	contacto=$(jq --arg nombre "$nombre" '.contactos | map(select(.nombre == $nombre)) | .[0]' $agenda_file)

	if [ "$contacto" != "null" ]; then
		# Eliminar el contacto del archivo JSON
		jq --arg nombre "$nombre" '.contactos |= map(select(.nombre != $nombre))' $agenda_file >temp.json && mv temp.json $agenda_file
		echo "Contacto eliminado con éxito."
	else
		echo "Contacto no encontrado."
	fi
	read -p "Presione enter para continuar..."
}

# Función para mostrar la lista de contactos
function mostrar_contactos() {
	clear
	# Obtener la lista de contactos del archivo JSON
	contactos=$(jq '.contactos' "$agenda_file")

	# Verificar si la lista de contactos no está vacía
	if [ -n "$contactos" ] && [ "$contactos" != "[]" ]; then
		echo "Contactos:"
		jq '.contactos' "$agenda_file"
	else
		echo "No hay contactos."
	fi

	read -p "Presione enter para continuar..."
}

# Menú principal

while true; do
	clear
	echo "Agenda de contactos"
	echo "Seleccione una opción:"
	echo "1) Agregar contacto"
	echo "2) Modificar contacto"
	echo "3) Eliminar contacto"
	echo "4) Mostrar contactos"
	echo "5) Salir"
	read opcion
	case "$opcion" in
	1)
		agregar_contacto
		;;
	2)
		modificar_contacto
		;;
	3)
		eliminar_contacto
		;;
	4)
		mostrar_contactos
		;;
	5)
		exit 0
		;;
	*)
		echo "Opción no válida."
		;;
	esac
done
