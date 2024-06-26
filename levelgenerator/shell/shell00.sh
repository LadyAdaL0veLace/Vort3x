#!/bin/bash

# Check if the script is run with root privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

username="shell00"

# Check if the user exists
if ! id "$username" &>/dev/null; then
    echo "User '$username' does not exist."
    exit 1
fi

# Create a readme.txt file
file="/home/$username/readme.txt"
echo "The Password to the next level is shell01" > $file
echo "readme.txt file has been created."

chmod 640 $file
chown shell01 $file
chgrp $username $file

