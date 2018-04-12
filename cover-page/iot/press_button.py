#!/usr/bin/python3

import requests
import cgitb
import sys
#import netrc
import os
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

sys.stderr = sys.stdout
cgitb.enable()
print("Content-Type:text/html;charset=utf-8\n\n")
print()
#print("<h1>You did it!</h1>")
#print("<p><a href=\"/iot/window.html\">Back</a>")
j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
content = "<h1>You did it!</h1><p><a href='window.html'>Back</a></p>"
print(j2_env.get_template("base.html").render(title='Internet of Things',content=content))

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

button_press = requests.put('https://academic-ni.cloud.thingworx.com/Thingworx/Things/myWindow_billchurch/Properties/*', headers=headers, params=params, data=data, auth=(username,password))
