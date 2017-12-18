import subprocess

subdomains = ["berlin","bethlehem","canaan","colebrook","gorham","groveton","haverhill","lancaster","milan","pittsburgh","stark","stewartstown","strafford","whitefield"]

ls_output = subprocess.check_output(['ls']).decode('utf-8')
contents = ls_output.splitlines()
# print(contents)

update_list = []

for town in subdomains:
	for name in contents:
		if name.find(town+'-') != -1:
			new_name = name.split('-')[1]
			update_list.append(town)
			# add date info for gallery folder nesting
			command = 'mv "' + name + '" "/var/www/html/wmsinh.org/public_html/' + name.split('-')[0] + '/gallery-source/' + new_name + '"'
			print(command)
			subprocess.call(command, shell=True)


#thumbs up gallery generation, only for those that were changed
for town in update_list:
	gallery_name = 'Pictures from ' + town.title()
	command = 'thumbsup --input /var/www/html/wmsinh.org/public_html/' + town + '/gallery-source/ --output /var/www/html/wmsinh.org/public_html/' + town + '/gallery --title "' + gallery_name + '"'
	print(command)
	subprocess.call(command, shell=True)