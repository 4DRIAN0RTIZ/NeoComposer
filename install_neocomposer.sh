#!/bin/bash

# Instalador de NeoComposer | NeoComposer installer
# Creado por 4DRIAN0RTIZ | Created by 4DRIAN0RTIZ

red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
reset="\033[0m"

GITHUB_RAW="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main"

function ctrl_c() {
	echo ""
	echo "** Instalación cancelada **"
	echo ""
	exit 1
}
trap ctrl_c INT

# Detect local vs remote execution (curl | bash sets BASH_SOURCE[0] to empty)
if [[ -n "${BASH_SOURCE[0]}" && "${BASH_SOURCE[0]}" != "bash" ]]; then
	SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
	if [[ -f "$SCRIPT_DIR/main.py" ]]; then
		MODE="local"
	else
		MODE="remote"
	fi
else
	MODE="remote"
	SCRIPT_DIR=""
fi

echo -e "${yellow}Modo: $MODE${reset}"

function obtener_distro() {
	distro=$(grep -m1 "^ID=" /etc/os-release | awk -F'=' '{ print $2 }' | tr -d '"')

	case "$distro" in
	"ubuntu" | "debian" | "linuxmint" | "kali")
		echo "apt-get"
		;;
	"fedora" | "centos" | "rhel")
		echo "dnf"
		;;
	"arch" | "manjaro")
		echo "pacman"
		;;
	*)
		echo "No se pudo detectar la distro"
		exit 1
		;;
	esac
}

manejador_paquetes=$(obtener_distro)

function instalar_paquete() {
	local pkg=$1
	echo -e "${yellow}Instalando $pkg...${reset}"
	case "$manejador_paquetes" in
	"pacman")
		sudo pacman -S "$pkg" --noconfirm
		;;
	*)
		sudo "$manejador_paquetes" install "$pkg" -y
		;;
	esac
}

declare -A dependencias=(
	["yazi"]="yazi"
	["nvim"]="neovim"
	["jq"]="jq"
	["python3"]="python3"
	["curl"]="curl"
)

for cmd in "${!dependencias[@]}"; do
	if ! command -v "$cmd" &>/dev/null; then
		echo -e "${yellow}$cmd no encontrado. Instalando...${reset}"
		instalar_paquete "${dependencias[$cmd]}"
		if [ $? -ne 0 ]; then
			echo -e "${red}Error al instalar $cmd${reset}"
			exit 1
		fi
	fi
done

install_dir="$HOME/.config/neocomposer"
mkdir -p "$install_dir"

archivos=(
	"main.py"
	"email_client.py"
	"agenda_manager.py"
	"config_manager.py"
	"mail_composer.py"
	"mail_sender.py"
	"requirements.txt"
	"agenda.sh"
	"agenda.json"
	"signature.html"
)

function obtener_archivo() {
	local archivo=$1
	if [[ "$MODE" == "local" ]]; then
		cp "$SCRIPT_DIR/$archivo" "$install_dir/"
	else
		echo -e "${yellow}Descargando $archivo...${reset}"
		curl -fsSL "$GITHUB_RAW/$archivo" -o "$install_dir/$archivo"
		if [ $? -ne 0 ]; then
			echo -e "${red}Error al descargar $archivo${reset}"
			exit 1
		fi
	fi
}

echo "Instalando archivos en $install_dir..."
for archivo in "${archivos[@]}"; do
	obtener_archivo "$archivo"
done

if [ ! -f "$install_dir/.env" ]; then
	if [[ "$MODE" == "local" ]]; then
		cp "$SCRIPT_DIR/env.example" "$install_dir/.env"
	else
		echo -e "${yellow}Descargando env.example...${reset}"
		curl -fsSL "$GITHUB_RAW/env.example" -o "$install_dir/.env"
	fi
fi

echo "Creando entorno virtual..."
python3 -m venv "$install_dir/venv"
if [ $? -ne 0 ]; then
	echo -e "${red}Error al crear entorno virtual${reset}"
	exit 1
fi

echo "Instalando dependencias Python..."
"$install_dir/venv/bin/pip" install -r "$install_dir/requirements.txt" -q
if [ $? -ne 0 ]; then
	echo -e "${red}Error al instalar dependencias Python${reset}"
	exit 1
fi

mkdir -p "$HOME/.local/bin"
rm -f "$HOME/.local/bin/neocomposer"
cat > "$HOME/.local/bin/neocomposer" << EOF
#!/bin/bash
exec "\$HOME/.config/neocomposer/venv/bin/python" "\$HOME/.config/neocomposer/main.py" "\$@"
EOF
chmod +x "$HOME/.local/bin/neocomposer"

echo -e "${green}Instalación completada. Ejecuta: neocomposer${reset}"
echo -e "${red}Configura tus credenciales en: $install_dir/.env${reset}"
