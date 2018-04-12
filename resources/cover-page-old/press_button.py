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

# store the information that we're waiting for confirmation...
subprocess.call('echo "waiting" > /var/www/html/wmsinh.org/public_html/flask/result.txt',shell=True)

print("Content-Type:text/html;charset=utf-8\n\n")
print()

j2_env = Environment(loader=FileSystemLoader(TEMP_DIR), trim_blocks=True)
content = """<h1>You did it!</h1>
            <p class="lead"><a href="/window.py" class="btn btn-lg btn-default">Back</a></p>"""
print(j2_env.get_template("base.html").render(title='Internet of Things',content=content,bgimg='../img/Network.png'))




os.putenv('HOME','/home/webpics')
os.environ['HOME'] = '/home/webpics'

with open('/home/webpics/pass/iot.txt', 'r') as myfile:
    username,password=myfile.read().replace('\n', '').split(',')

# get our username and password from the secure .netrc file
#HOST = "academic-ni.cloud.thingworx.com"
#secrets = netrc.netrc()
#username, account, password = secrets.authenticators(HOST)

headers = {'Accept': 'application/json AppKey:ba063966-5d0d-46ff-be4f-2a9ace0f40a0 Content-Type:application/json'}

params = (
            ('Accept', 'application/json-compressed'),
                ('_twsr', '1'),
                    ('Content-Type', 'application/json'),
                    )

data = '{"visitorButtonClicked":true}'

# button_press = requests.put('https://academic-ni.cloud.thingworx.com/Thingworx/Things/myWindow_billchurch/Properties/*', headers=headers, params=params, data=data, auth=(username,password))
button_press = requests.put('http://althor.net/t.pl', headers=headers, params=params, data=data, auth=(username,password))
