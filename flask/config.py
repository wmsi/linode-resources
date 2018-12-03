import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Config settings for the flask application. Turn debug notifications on and set\
# the URL of our database on the server. When running this app in a local dev
# environment you need to comment out the SERVER_NAME
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SERVER_NAME = "wmsinh.org" # server hostname required  for subdomain support

#### Important: install flask_moment and test new datetime handling before pushing to git