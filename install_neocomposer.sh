#!/bin/bash

# Instalador de NeoComposer | NeoComposer installer
# Creado por 4DRIAN0RTIZ | Created by 4DRIAN0RTIZ

# Colores ANSI
red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
blue="\033[1;34m"
reset="\033[0m"

function ctrl_c() {
	echo ""
	echo "** Matando proceso **"
	echo ""
	exit 1
}
trap ctrl_c INT

# Comprobar distro | Check distro

function obtener_distro() {
	distro=$(grep -m1 "^ID=" /etc/os-release | awk -F'=' '{ print $2 }' | tr -d '"')

	case "$distro" in
	"ubuntu" | "debian" | "linuxmint" | "kali")
		echo "apt-get"
		;;
	"fedora" | "centos" | "rhel")
		echo "dnf"
		;;
	"arch")
		echo "pacman"
		;;
	*)
		echo "No se pudo detectar la distro"
		exit 1
		;;
	esac
}

manejador_paquetes=$(obtener_distro)

# Verificación de dependencias
declare -A dependencias=(
	["ranger"]="sudo $manejador_paquetes install ranger -y"
	["nvim"]="sudo $manejador_paquetes install neovim -y"
	["jq"]="sudo $manejador_paquetes install jq -y"
	["python3"]="sudo $manejador_paquetes install python-is-python3 -y"
)

for dependencia in "${!dependencias[@]}"; do
	if ! command -v "$dependencia" &>/dev/null; then
		echo "El comando '$dependencia' no está instalado"
		echo "Instalando '$dependencia'..."
		eval "${dependencias[$dependencia]}"
		if [ $? -ne 0 ]; then
			echo "Error al instalar '$dependencia'"
			exit 1
		fi
	fi
done

# Directorio de instalación | Installation directory
install_dir="$HOME/.config/neocomposer"
mkdir -p $install_dir

# Archivos necesarios | Necesary files
declare -A archivos_a_descargar=(
	["main.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main/main.py"
	["email_client.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main/email_client.py"
	["email_functions.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main/email_functions.py"
	["requirements.txt"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main/requirements.txt"
	["env.example"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main/env.example"
	["agenda.json"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main/agenda.json"
	["agenda.sh"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main/agenda.sh"
	["signature.html"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main/signature.html"
)

# Descargando archivos | Downloading files

for archivo in "${!archivos_a_descargar[@]}"; do
	if [ ! -f "$archivo" ]; then
		echo "Descargando $archivo..."
		wget -q "${archivos_a_descargar[$archivo]}"
		if [ $? -ne 0 ]; then
			echo "Error al descargar $archivo"
			exit 1
		fi
	fi
done

# Permitiendo ejecución de NeoComposer.py | Allowing execution of NeoComposer.py
echo "Permitiendo ejecución de NeoComposer.py..."
chmod +x NeoComposer.py

# Instalando dependencias de Python | Installing Python dependencies
echo "Instalando dependencias de Python..."
pip install -r requirements.txt

# Moviendo archivos a directorio | Moving files to directory
echo "Moviendo archivos a directorio..."
cp main.py "$install_dir"
cp email_client.py "$install_dir"
cp email_functions.py "$install_dir"
cp env.example "$install_dir/.env"
cp agenda.sh "$install_dir"
cp agenda.json "$install_dir"
cp signature.html "$install_dir"

# Crear acceso directo | Create shortcut
echo "Creando acceso directo..."
ln -s "$install_dir/main.py" "$HOME/.local/bin/neocomposer"

echo -e "${green}Instalación completada | Ejecuta neocomposer para iniciar${reset}"
echo -e "${red}No olvides configurar el archivo $install_dir/.env${reset}"
