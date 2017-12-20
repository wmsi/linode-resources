#!/usr/bin/python3

import requests
import cgitb
import sys
#import netrc
import os
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import subprocess

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.dirname(os.path.join(THIS_DIR, 'templates/'))

sys.stderr = sys.stdout
cgitb.enable()

print("Content-Type:text/html;charset=utf-8\n\n")
print()

with open('status.txt', 'r') as file:
    status=file.read().replace('\n', '')
# status = str(file.read())

if(status.find('success') != -1):
	print("success page")
else:
	print("waiting page")

# j2_env = Environment(loader=FileSystemLoader(TEMP_DIR), trim_blocks=True)
# content = """<h1>You did it!</h1>
#             <p class="lead"><a href="/window.py" class="btn btn-lg btn-default">Back</a></p>"""
# print(j2_env.get_template("base.html").render(title='Internet of Things',content=content,bgimg='../img/Network.png'))

