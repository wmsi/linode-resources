#!/usr/bin/python3

# Various utility functions for the Flask app

import datetime
import babel

# double check this function for timestamp discrepancies with the web page (JS)
    # Returns the current UNIX timestamp - based on 
    # https://stackoverflow.com/a/19801863 and confirmed
    # at 'man strftime1' on linux
def get_cur_timestamp():
    return datetime.datetime.now().strftime("%s")

    # format dates as either full or medium format
    # Currently this utility is used by the Jinja2 template
    # in data_story.html. The utility is set to correspond with
    # the "datetime" filter in flasktest.py
def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm:ss"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm:ss"
    return babel.dates.format_datetime(value, format)

# def format_datetime_iso(value)
#     format=
