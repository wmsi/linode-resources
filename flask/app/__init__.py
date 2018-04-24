# File used to define a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
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
login.login_view = 'login'
handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

DEFAULT_SUBDOMAIN = "www"

from app import routes
