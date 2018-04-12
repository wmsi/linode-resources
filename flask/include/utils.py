#!/usr/bin/python3

# Various utility functions for the Flask app

import datetime
import babel

def get_cur_timestamp():
    """ Returns the current UNIX timestamp - based on 
        https://stackoverflow.com/a/19801863 and confirmed
        at 'man strftime1' on linux"""
    return datetime.datetime.now().strftime("%s")

def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm:ss"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm:ss"
    return babel.dates.format_datetime(value, format)