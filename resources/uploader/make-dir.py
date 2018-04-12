# This script can be repurposed for file management tasks across all subdomains

import subprocess

subdomains = ["berlin","bethlehem","canaan","colebrook","gorham","groveton","haverhill","lancaster","milan","pittsburgh","stark","stewartstown","strafford","whitefield"]

ls_output = subprocess.check_output(['ls']).decode('utf-8')
contents = ls_output.splitlines()
# print(contents)

for town in subdomains:
	for folder in contents:
		if town == folder:
			command1 = "mkdir " + folder + "/gallery-source"
			# print(command1)
			# subprocess.call(command1, shell=True)
			command2 = "cp index-redirect.html " + folder + "/index.html"
			# print(command2)
			# subprocess.call(command2, shell=True)
			command3 = 'rm -r ' + folder + '"/gallery-source/Test Album/"'
			subprocess.call(command3, shell=True)
