#!/bin/bash

# Check if the script is run with root privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

username="shell02"

# Check if the user exists
if ! id "$username" &>/dev/null; then
    echo "User '$username' does not exist."
    exit 1
fi

# Create a directory named inhere in the user's home directory
dir="/home/$username/inhere"
mkdir $dir
echo "Directory named 'inhere' has been created in the user's home directory."

# Create a file named .hidden in the directory inhere
file="$dir/.hidden"
echo "The password to the next level is shell03" > $file
echo "File named '.hidden' has been created in 'inhere' directory."

chmod 755 $dir
chown root:root $dir

chmod 640 $file
chown shell03:$username $file
