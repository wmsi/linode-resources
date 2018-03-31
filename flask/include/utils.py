#!/usr/bin/python3

# Various utility functions for the Flask app

import datetime

def get_cur_timestamp():
    """ Returns the current UNIX timestamp - based on 
        https://stackoverflow.com/a/19801863 and confirmed
        at 'man strftime1' on linux"""
    return datetime.datetime.now().strftime("%s")
