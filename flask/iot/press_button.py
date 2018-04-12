#!/usr/bin/python

# This script is the magic behind our Internet of Things example. It should be linked on the server from window.py, or whatever welcome page we have for this part of the site. When this script gets executed it will write a timestamp to the status file, render the HTML page, and post a button press to thingworx.com. Then Labview can see the changed button state on thingworx and make the EV3 do something.

import requests
import cgitb
import sys
import os
from jinja2 import Environment, FileSystemLoader
import subprocess
import datetime, time
from include.utils import *
from include.config import *

# maintain backwards compatibility with CGI...
sys.stderr = sys.stdout
cgitb.enable()

# store the timestamp in the status.txt file
def timeStamp():
	subprocess.call('echo "%s" > %s' % \
	    (str(get_cur_timestamp()), IOT_STATUS_FILE), shell=True)

# print a header so the browser doesn't freak out (only required when using CGI)
def printHeader():
	print("Content-Type:text/html;charset=utf-8\n\n")
	print()

# get the thingworx password from file
def getPassword():
	os.putenv('HOME','/home/webpics')
	os.environ['HOME'] = '/home/webpics'

	with open('/home/webpics/pass/iot.txt', 'r') as myfile:
	    username,password=myfile.read().replace('\n', '').split(',')
	   
	return username, password;

# put together an HTTP request and send it to thingworx
def sendRequest():
	username, password = getPassword()
	
	headers = {'Accept': 'application/json AppKey:ba063966-5d0d-46ff-be4f-2a9ace0f40a0 Content-Type:application/json'}

	params = (
	            ('Accept', 'application/json-compressed'),
	                ('_twsr', '1'),
	                    ('Content-Type', 'application/json'),
	                    )

	data = '{"visitorButtonClicked":true}'

	button_press = requests.put('https://academic-ni.cloud.thingworx.com/Thingworx/Things/myWindow_billchurch/Properties/*', headers=headers, params=params, data=data, auth=(username,password))

if __name__ == "__main__":
	timeStamp()
	printHeader()
	sendRequest()

