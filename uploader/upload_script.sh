#!/bin/bash
clear

printf "=========================================================================================
This script takes files from your harddrive and uploads them to the WMSI Linode-based 
server. The files will the appear in the \"webpics\" account on our Linode.
Note that by default this script will autogenerate a folder named with today's date.
New uploads will appear in \"/home/webpics/uploads/[date]\" and from there can be moved 
elsewhere on the server. 

If you find yourself uploading pictures multiple times a day you may want to change 
this setting to keep them separate. Simply edit the date format string in the last line 
of this file or create your own naming convention.


Press [Enter] to continue.
=========================================================================================\n\n"

read -s

printf "\n\n\n
=========================================================================================
What is the relative path (starting in this folder) of the directory containing your images? 
If you want to upload this entire folder enter \".\", otherwise enter \"./[path]\". 
E.g. \"./Camps/July_17\"
========================================================================================\n\n"

read FROM_PATH

# check if the path is empty or contains only spaces
while [[ -z "${FROM_PATH// }" ]]
do
	printf "\n\nPlease enter a non-empty string for the path."
	read FROM_PATH
done

printf "\n\nrsync -azvhe ssh $FROM_PATH/* webpics@45.79.101.26:/home/webpics/uploads/$(date '+%d-%b-%Y')\n\n"

sshpass -f <(printf '%s\n' 0wms1L1node) rsync -azvhe ssh $FROM_PATH/* webpics@45.79.101.26:/home/webpics/uploads/$(date '+%d-%b-%Y')
