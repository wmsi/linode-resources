#!/usr/bin/python3

# move-uploads.py
# This script should be run automatically on the server to move new albums into their subdomains and generate galleries. To check if this script is scheduled to run type 'crontab -l' while signed in as the webpics user

import subprocess
import datetime 
import os

THUMBSUP_SITES_DIREC = '/var/www/html/wmsinh.org/public_html/thumbsup_sites'

subdomains = [name for name in os.listdir(THUMBSUP_SITES_DIREC) if os.path.join('.', name)]
# ["berlin","bethlehem","canaan","colebrook","gorham","groveton","haverhill","lancaster","milan","pittsburgh","stark","stewartstown","strafford","whitefield"]

ls_output = subprocess.check_output(['ls']).decode('utf-8')
contents = ls_output.splitlines()
# print(contents)

update_list = []

for town in subdomains:
	for name in contents:
		if name.find(town+'-') != -1:
			new_name = name.replace(town+'-','')
			update_list.append(town)
			if(new_name[0].isdigit()):
				# pull off the year to properly nest the folder
				year, new_name = new_name.split('-')
			else:
				# otherwise use the current year
				year = str(datetime.datetime.now().year)
			# add date info for gallery folder nesting
			command = 'mv -p "%s" "%s/%s/gallery-source/%d/%s"' % (name, THUMBSUP_SITES_DIREC, town, year, new_name)
			# print(command)
			subprocess.call(command, shell=True)


#thumbs up gallery generation, only for those that were changed
for town in update_list:
	gallery_name = 'Pictures from ' + town.title()
	gallery_loc = THUMBSUP_SITES_DIREC + '/' + town
	command = 'thumbsup --config thumbsup-global-config.json --input "%s/gallery-source/" --output "%s/gallery" --title "%s"' % (gallery_loc, gallery_loc, gallery_name)
	
	# print(command)
	subprocess.call(command, shell=True)
