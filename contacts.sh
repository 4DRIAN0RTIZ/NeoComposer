#!/bin/bash

# Script that manages NeoComposer's contacts list.
# Author: 4DRIAN0RTIZ
# Date: 19/08/2023
# Description: This script allows adding, editing, and removing contacts.

# Name of the file that holds the contacts
contacts_file="$HOME/.config/neocomposer/contacts.json"

# Function to add a new contact
function add_contact() {
	clear
	echo "Enter the contact's name or alias:"
	read name
	echo "Enter the contact's email address:"
	read email

	# Add the new contact to the JSON file
	jq --arg name "$name" --arg email "$email" '.contacts += [{"name": $name, "email": $email}]' $contacts_file >tmp.$$.json && mv tmp.$$.json $contacts_file

	echo "Contact added successfully."
	read -p "Press enter to continue..."
}

# Function to edit an existing contact

function edit_contact() {
	clear
	echo "Enter the name or alias of the contact to edit:"
	read name

	# Look up the contact in the JSON file
	contact=$(jq --arg name "$name" '.contacts | map(select(.name == $name)) | .[0]' $contacts_file)

	# If the contact exists, show its data and ask for the new values
	if [ -n "$contact" ]; then
		echo "Current data:"
		echo $contact | jq

		# Ask which field to edit
		echo "Which field do you want to edit?"
		read -p "1) Name, 2) Email, 3) Both: " option

		case "$option" in
		1)
			echo "Enter the new name:"
			read new_name
			jq --arg name "$name" --arg new_name "$new_name" \
				'.contacts |= map(if .name == $name then . + {"name": $new_name} else . end)' \
				"$contacts_file" >temp.json && mv temp.json "$contacts_file"
			echo "Name updated successfully."
			;;
		2)
			echo "Enter the new email:"
			read new_email
			jq --arg name "$name" --arg new_email "$new_email" \
				'.contacts |= map(if .name == $name then . + {"email": $new_email} else . end)' \
				"$contacts_file" >temp.json && mv temp.json "$contacts_file"
			echo "Email updated successfully."
			;;
		3)
			echo "Enter the new name:"
			read new_name
			echo "Enter the new email:"
			read new_email
			jq --arg name "$name" --arg new_name "$new_name" --arg new_email "$new_email" \
				'.contacts |= map(if .name == $name then . + {"name": $new_name, "email": $new_email} else . end)' \
				"$contacts_file" >temp.json && mv temp.json "$contacts_file"
			echo "Name and email updated successfully."
			;;
		*)
			echo "Invalid option. No changes were made."
			;;
		esac
	else
		echo "Contact not found."
	fi
	read -p "Press enter to continue..."
}

# Function to remove an existing contact

function remove_contact() {
	clear
	echo "Enter the name or alias of the contact to remove:"
	read name

	# Check whether the contact exists
	contact=$(jq --arg name "$name" '.contacts | map(select(.name == $name)) | .[0]' $contacts_file)

	if [ "$contact" != "null" ]; then
		# Remove the contact from the JSON file
		jq --arg name "$name" '.contacts |= map(select(.name != $name))' $contacts_file >temp.json && mv temp.json $contacts_file
		echo "Contact removed successfully."
	else
		echo "Contact not found."
	fi
	read -p "Press enter to continue..."
}

# Function to show the contact list
function show_contacts() {
	clear
	# Get the contact list from the JSON file
	contacts=$(jq '.contacts' "$contacts_file")

	# Check whether the contact list is not empty
	if [ -n "$contacts" ] && [ "$contacts" != "[]" ]; then
		echo "Contacts:"
		jq '.contacts' "$contacts_file"
	else
		echo "No contacts."
	fi

	read -p "Press enter to continue..."
}

# Main menu

while true; do
	clear
	echo "Contacts"
	echo "Select an option:"
	echo "1) Add contact"
	echo "2) Edit contact"
	echo "3) Remove contact"
	echo "4) Show contacts"
	echo "5) Exit"
	read option
	case "$option" in
	1)
		add_contact
		;;
	2)
		edit_contact
		;;
	3)
		remove_contact
		;;
	4)
		show_contacts
		;;
	5)
		exit 0
		;;
	*)
		echo "Invalid option."
		;;
	esac
done
