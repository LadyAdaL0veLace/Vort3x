## Users and groups

`ls -l /home` Check for users on the operating system

`cat etc/passwd` Shows all the users on the operating system. Pipe thorough `wc -l` to get a number of total users on the operating system.

## Add and remove user with home directory

`sudo useradd <username>` Add a new user without the home directory

`sudo useradd -m <username>` Add a new user with the home directory

`sudo userdel <username>` Remove the user without the home directory

`sudo userdel -r <username>` Remove the user and associated home directory

## Add password

`sudo passwd <new password>`
