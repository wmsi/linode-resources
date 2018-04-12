from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ForumForm(FlaskForm):
	email = StringField('Email Address:', validators=[DataRequired()]) # add email address validators
	user = StringField('Username:')
	post = TextAreaField('Post Content:', validators=[DataRequired()])
	submit = SubmitField('Post!')

class FrameForm(FlaskForm):
	url1 = StringField('URL:', validators=[DataRequired()])
	url2 = StringField('URL:')
	url3 = StringField('URL:')
	url4 = StringField('URL:')
	submit = SubmitField('Generate Gallery!')