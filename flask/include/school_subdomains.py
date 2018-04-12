#!/usr/bin/python
# Handles management and serving of school subdomains,
# including integrating with the generated thumbsup site
# Mckenna Cisler <mckennacisler@gmail.com>

from flask import abort, send_from_directory
from include.config import *

SCHOOL_SUBDOMAIN_FOLDER = "/var/www/html/wmsinh.org/public_html/thumbsup_sites/" # trailing slash!

def serve_school_subdomain(subdomain, filename):
    if subdomain not in SCHOOL_SUBDOMAINS:
        print("subdomain404")
        abort(404)
    else:
        direc = SCHOOL_SUBDOMAIN_FOLDER + subdomain + "/gallery/"
        print(direc, filename)
        return send_from_directory(direc, filename)

