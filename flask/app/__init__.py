# File used to define a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from airtable import Airtable
# from flask_socketio import SocketIO, emit
from config import Config
from include.credentials import *
import logging
from logging.handlers import RotatingFileHandler

app=Flask(__name__)
Config.SECRET_KEY = SECRET_KEY          # so that SECRET_KEY can be stored in secure credentials.py file
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
login = LoginManager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
base = Airtable('app2FkHOwb0jN0G8v','Activities', api_key=AIRTABLE_API_KEY)
base.get_all(view='Grid View', maxRecords=20)
print('got some records')

login.login_view = 'login'
handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

DEFAULT_SUBDOMAIN = "www"

from app import routes

