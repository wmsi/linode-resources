#!/usr/bin/env python

import requests
outfile = requests.get('https://gorham.wmsinh.org/testcgi/outfile.txt')
outfile_text = outfile.text
commands = list(filter(None,outfile_text.split('\n')))
print(commands)