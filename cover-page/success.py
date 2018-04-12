#!/usr/bin/python3

# Render a success page for after the EV3 has done something. Python scripts such as this one should become unnecessary soon as we move towards hosting everything with Flask.

import requests
import sys
import os
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.dirname(os.path.join(THIS_DIR, 'templates/'))

sys.stderr = sys.stdout
print("Content-Type:text/html;charset=utf-8\n\n")
print()

content = """ 
<h1>Success!</h1>
<p class="lead">You are now a part of the WMSI node in the Internet of Things! Go back to the Window page or continue exploring our site</p>
<p class="lead"><a href="../window.py" class="btn btn-lg btn-default">BACK</a></p>

"""

j2_env = Environment(loader=FileSystemLoader(TEMP_DIR), trim_blocks=True)
print(j2_env.get_template("base.html").render(title='Internet of Things', bgimg='../img/Network.png', content=content))

