#!/usr/bin/python3

# Use this script to update all galleries with the image files in [subdomain]/gallery-source. You will most likely want to use this if you manually put a new album in gallery-source or if you deleted content from gallery-source and want to display changes online.

import subprocess
import os

# subdomains = ["berlin","bethlehem","canaan","colebrook","gorham","groveton","haverhill","lancaster","milan","pittsburgh","stark","stewartstown","stratford","whitefield"]
THUMBSUP_SITES_DIREC = '/var/www/html/wmsinh.org/public_html/thumbsup_sites'
subdomains = [name for name in os.listdir(THUMBSUP_SITES_DIREC) if os.path.isdir(os.path.join(THUMBSUP_SITES_DIREC, name, 'gallery-source'))]

#thumbs up gallery generation, only for those that were changed
for town in subdomains:
	gallery_name = 'Pictures from ' + town.title()
	gallery_loc = THUMBSUP_SITES_DIREC + '/' + town
	command = 'thumbsup --config thumbsup-global-config.json --input "%s/gallery-source/" --output "%s/gallery" --title "%s"' % (gallery_loc, gallery_loc, gallery_name)
	# print(command)
	subprocess.call(command, shell=True)
