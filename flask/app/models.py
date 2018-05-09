from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin	

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	wmsi_user = db.Column(db.Boolean, default=False)
	data_story = db.Column(db.Boolean, default=False)	# while in dev this will only be true for wmsi users
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def set_password(self, password):
		self.password_hash= generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)

class DataStory(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	project_id = db.Column(db.Integer)
	sensor_id = db.Column(db.Integer)
	data_type = db.Column(db.String)
	value = db.Column(db.Float)

	def __repr__(self):
		return '<DataStory %s, %s>' % (str(self.project_id), str(self.timestamp)) # format datetime

@login.user_loader
def load_user(id):
	return User.query.get(int(id))