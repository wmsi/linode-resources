import subprocess

subdomains = ["berlin","bethlehem","canaan","colebrook","gorham","groveton","haverhill","lancaster","milan","pittsburgh","stark","stewartstown","strafford","whitefield"]

#thumbs up gallery generation, only for those that were changed
for town in subdomains:
	gallery_name = 'Pictures from ' + town.title()
	command = 'thumbsup --input /var/www/html/wmsinh.org/public_html/' + town + '/gallery-source/ --output /var/www/html/wmsinh.org/public_html/' + town + '/gallery --title "' + gallery_name + '"'
	print(command)
	subprocess.call(command, shell=True)