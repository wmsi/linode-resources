#!/usr/bin/python
# from flask import Flask, request, render_template, send_file, redirect, url_for
from app import app,db
from app.models import User, Post, DataStory
import subprocess
import iot.press_button as pressButton
from include.utils import *
from include.config import *
from include.school_subdomains import *

# app.run()

@app.shell_context_processor
def make_shell_contact():
	return{'db':db, 'User': User,'Post': Post, 'DataStory': DataStory}

# See __init__.py for global constants

# app=Flask(__name__)
# app.config["DEBUG"] = True
# app.config["SERVER_NAME"] = "wmsinh.org" # server hostname required for subdomain support

# DEFAULT_SUBDOMAIN = "www"

### PAGE ROUTES ###

# @app.route("/")
# def index():
#     return render_template('index.html')
    
# @app.route("/mobile")
# def mobile():
#     return render_template('mobile.html', 
#         title="Mobile Programs")

# @app.route("/all-locations")
# def locations():
#     return render_template('all-locations.html',    
#         title="All WMSI Locations")

# ### SCHOOL SUBDOMAIN ROUTES ###

# # for, now always redirect to the gallery index for school subdomains
# # (note: this must route /gallery/ with a _specific trailing
# # slash_ to the index, because the various files in 
# # gallery will redirect to gallery/ with the slash, and
# # flask will return a 404 if we don't add that slash here
# # (see here: http://flask.pocoo.org/docs/0.12/quickstart/#variable-rules))
# @app.route("/", subdomain="<site_subdomain>")
# def school_index(site_subdomain):
#     return redirect("/gallery/") # direct redirect below

# # make sure the root page displays the index
# @app.route("/gallery/", subdomain="<site_subdomain>")
# def subdomain_index(site_subdomain):
#     return school_subdomain(site_subdomain, "index.html")

# # any requests to gallery items for each subdomain are passed
# # onto the correct school domain subfolder
# # (thumbs up stores files and SETS LINKS assuming that 
# #  files are stored under /gallery/, so we serve files 
# #  statically (from the filesystem) from there)
# @app.route("/gallery/<path:filename>", subdomain="<site_subdomain>")
# def school_subdomain(site_subdomain, filename):
#     if site_subdomain == DEFAULT_SUBDOMAIN: # www
#         return redirect(url_for('index'))
#     else:
#         return serve_school_subdomain(site_subdomain, filename)

# ### IOT ROUTES ###

# @app.route("/window")
# def window():
#     return render_template("iot-window.html", \
#         title='Internet of Things', bgimg='static/img/Network.png')

# @app.route("/press_button")
# def pressbutton():
#     pressButton.timeStamp()
#     pressButton.sendRequest()
#     return render_template('iot-waiting.html', \
#         title='Internet of Things', bgimg='static/img/Network.png')

# @app.route("/success")
# def success():
#     return render_template("iot-success.html", \
#         title='Internet of Things', bgimg='static/img/Network.png')

# @app.route("/labview", methods=['POST'])
# def labview():
#     subprocess.call('echo "%s" >> %s' \
#         % (str(request.values['time']), IOT_STATUS_FILE), shell=True)
#     print("from labview post: " + str(request.values['time']))
#     return "Hello Labview\n"
    
# @app.route("/iot/status")
# def status():
#     return send_file(IOT_STATUS_FILE, cache_timeout=0.5) # disable caching (mostly)

# ### SPECIAL ###

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404

# # Run server when this file is executed

# if __name__ == "__main__":
#     app.run()
    
