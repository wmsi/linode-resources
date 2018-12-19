#!/usr/bin/python
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from app import app, db, moment
from app.models import User, Post, DataStory
import subprocess
import iot.press_button as pressButton
from include.utils import *
from include.school_subdomains import *

app.jinja_env.filters['datetime'] = format_datetime
# app.jinja.filters['datetime'] = format_datetime

# add the database instance and models to the shell context. This allows
# you to work directly with the databalse by running "flask shell" from
# the command line.
@app.shell_context_processor
def make_shell_contact():
    return{'db':db, 'User': User,'Post': Post, 'DataStory': DataStory, 'moment':moment}
