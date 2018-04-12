#!/usr/bin/python3

# This simply renders a web page for the window example. After some more development work we should be able to have Flask handle this instead of having an individual python script for every web page

import sys
#import netrc
import os
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.dirname(os.path.join(THIS_DIR, 'templates/'))

sys.stderr = sys.stdout
print("Content-Type:text/html;charset=utf-8\n\n")
print()

j2_env = Environment(loader=FileSystemLoader(TEMP_DIR), trim_blocks=True)
print(j2_env.get_template("window.html").render(title='Internet of Things', bgimg='../img/Network.png'))

