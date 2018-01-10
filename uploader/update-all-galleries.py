#!/usr/bin/python3

# Use this script to update all galleries with the image files in [subdomain]/gallery-source. You will most likely want to use this if you manually put a new album in gallery-source or if you deleted content from gallery-source and want to display changes online.

import subprocess
import os

# subdomains = ["berlin","bethlehem","canaan","colebrook","gorham","groveton","haverhill","lancaster","milan","pittsburgh","stark","stewartstown","stratford","whitefield"]
path = '/var/www/html/wmsinh.org/public_html'
subdomains = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name, 'gallery-source'))]

#thumbs up gallery generation, only for those that were changed
for town in subdomains:
	gallery_name = 'Pictures from ' + town.title()
	command = 'thumbsup --input /var/www/html/wmsinh.org/public_html/' + town + '/gallery-source/ --output /var/www/html/wmsinh.org/public_html/' + town + '/gallery --title "' + gallery_name + '"'
	# print(command)
 	subprocess.call(command, shell=True)
