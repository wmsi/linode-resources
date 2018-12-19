from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin	

# create a class for Users in the database. Include attributes for WMSI users and
# users with access to the data-story page. For security purposes only store the
# password hash in the database. This class makes use of UserMixin to add support
# for flask_login functions
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	wmsi_user = db.Column(db.Boolean, default=False)
	data_story = db.Column(db.Boolean, default=False)	# while in dev this will be true for all users
	# This attribute is added to by the forum pages (dev)
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	# store the password hash for a new user password in the database
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	# check the hash of a submitted user password against the one in the database
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	# tell python how to print objects of this class. For now this set to only print the username
	def __repr__(self):
		return '<User {}>'.format(self.username)

# Class for data stored with the Digital Data Stories project. 
# Potential imrpovements:
#	- Attach all data story posts to users
#	- Check for discrepancy between datetime.utcnow anc the datetime in data-story
class DataStory(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	project_id = db.Column(db.Integer, db.ForeignKey('project_meta_data.id'))
	sensor_id = db.Column(db.Integer, default=0)
	data_type = db.Column(db.String(64))
	value = db.Column(db.Float)
	archived = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return '<DataStory %s, %s>' % (str(self.project_id), str(self.timestamp)) # format datetime

# Store meta data about each Data Story project in the database.
# The goal is for larger data types (such as strings) associated with projects to be 
# stored in this format
class ProjectMetaData(db.Model):
	id = db.Column(db.Integer, primary_key=True) # db.ForeignKey('datastory.project_id'), 
	# project_id = db.Column(db.Integer, db.ForeignKey(datastory.project_id))
	project_name = db.Column(db.String(64))
	description = db.Column(db.String(500))		# formal explanation of project abstract
	miscellaneous = db.Column(db.String(160))	# this can be a place to write equipment used, classroom, data types, etc.
	data = db.relationship('DataStory', backref='metadata', lazy='dynamic')

	def __repr__(self):
		return '<ProjectMetaData %s, %s>' % (str(self.id), str(self.project_name))


# create a class for Posts in the database. Posts are always attahed to a User
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)

# Point the flask_login functions toward the correct user in the database
@login.user_loader
def load_user(id):
	return User.query.get(int(id))
