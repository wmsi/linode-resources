#!/usr/bin/python
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from app import app,db
from app.models import User, Post, DataStory
import subprocess
import iot.press_button as pressButton
from include.utils import *
from include.school_subdomains import *

app.jinja_env.filters['datetime'] = format_datetime

@app.shell_context_processor
def make_shell_contact():
    return{'db':db, 'User': User,'Post': Post, 'DataStory': DataStory}
