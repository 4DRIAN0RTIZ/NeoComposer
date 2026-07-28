#!/bin/bash

# NeoComposer installer
# Created by 4DRIAN0RTIZ

red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
reset="\033[0m"

GITHUB_REPO="https://github.com/4DRIAN0RTIZ/NeoComposer.git"
GITHUB_RAW="https://raw.githubusercontent.com/4DRIAN0RTIZ/NeoComposer/main"

function ctrl_c() {
	echo ""
	echo "** Installation cancelled **"
	echo ""
	exit 1
}
trap ctrl_c INT

# Detect local vs remote execution (curl | bash sets BASH_SOURCE[0] to empty)
if [[ -n "${BASH_SOURCE[0]}" && "${BASH_SOURCE[0]}" != "bash" ]]; then
	SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
	if [[ -f "$SCRIPT_DIR/pyproject.toml" ]]; then
		MODE="local"
	else
		MODE="remote"
	fi
else
	MODE="remote"
	SCRIPT_DIR=""
fi

echo -e "${yellow}Mode: $MODE${reset}"

function detect_distro() {
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
		echo "Could not detect the distro"
		exit 1
		;;
	esac
}

package_manager=$(detect_distro)

function install_package() {
	local pkg=$1
	echo -e "${yellow}Installing $pkg...${reset}"
	case "$package_manager" in
	"pacman")
		sudo pacman -S "$pkg" --noconfirm
		;;
	*)
		sudo "$package_manager" install "$pkg" -y
		;;
	esac
}

declare -A dependencies=(
	["yazi"]="yazi"
	["nvim"]="neovim"
	["jq"]="jq"
	["python3"]="python3"
	["curl"]="curl"
	["git"]="git"
)

for cmd in "${!dependencies[@]}"; do
	if ! command -v "$cmd" &>/dev/null; then
		echo -e "${yellow}$cmd not found. Installing...${reset}"
		install_package "${dependencies[$cmd]}"
		if [ $? -ne 0 ]; then
			echo -e "${red}Error installing $cmd${reset}"
			exit 1
		fi
	fi
done

install_dir="$HOME/.config/neocomposer"
mkdir -p "$install_dir"
mkdir -p "$install_dir/templates"

# Non-package files: user data / standalone tooling, not shipped inside the
# neocomposer Python package, so they are installed as loose files.
support_files=(
	"contacts.sh"
	"contacts.json"
)

function fetch_support_file() {
	local file=$1
	if [[ "$MODE" == "local" ]]; then
		cp "$SCRIPT_DIR/$file" "$install_dir/"
	else
		echo -e "${yellow}Downloading $file...${reset}"
		curl -fsSL "$GITHUB_RAW/$file" -o "$install_dir/$file"
		if [ $? -ne 0 ]; then
			echo -e "${red}Error downloading $file${reset}"
			exit 1
		fi
	fi
}

echo "Installing support files in $install_dir..."
for file in "${support_files[@]}"; do
	fetch_support_file "$file"
done

if [ ! -f "$install_dir/.env" ]; then
	if [[ "$MODE" == "local" ]]; then
		cp "$SCRIPT_DIR/env.example" "$install_dir/.env"
	else
		echo -e "${yellow}Downloading env.example...${reset}"
		curl -fsSL "$GITHUB_RAW/env.example" -o "$install_dir/.env"
	fi
fi

echo "Creating virtual environment..."
python3 -m venv "$install_dir/venv"
if [ $? -ne 0 ]; then
	echo -e "${red}Error creating virtual environment${reset}"
	exit 1
fi

echo "Installing the neocomposer package..."
if [[ "$MODE" == "local" ]]; then
	"$install_dir/venv/bin/pip" install "$SCRIPT_DIR" -q
else
	package_src_dir=$(mktemp -d)
	git clone --depth 1 "$GITHUB_REPO" "$package_src_dir" -q
	if [ $? -ne 0 ]; then
		echo -e "${red}Error cloning the repository${reset}"
		exit 1
	fi
	"$install_dir/venv/bin/pip" install "$package_src_dir" -q
	rm -rf "$package_src_dir"
fi
if [ $? -ne 0 ]; then
	echo -e "${red}Error installing the neocomposer package${reset}"
	exit 1
fi

mkdir -p "$HOME/.local/bin"
rm -f "$HOME/.local/bin/neocomposer"
ln -sf "$install_dir/venv/bin/neocomposer" "$HOME/.local/bin/neocomposer"

echo -e "${green}Installation complete. Run: neocomposer${reset}"
echo -e "${red}Set up your credentials in: $install_dir/.env${reset}"
