from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DataForm(FlaskForm):
    project_id = IntegerField(validators=[DataRequired])
    data_type = StringField(validators=[DataRequired])
    value = IntegerField(validators=[DataRequired])

class ForumForm(FlaskForm):
	# email = StringField('Email Address:', validators=[DataRequired()]) # add email address validators
	# user = StringField('Username:')
	body = TextAreaField('Post Content:', validators=[DataRequired()])
	submit = SubmitField('Post!')

class EditForm(FlaskForm):
	delete = BooleanField('Delete')
	submit = SubmitField('Delete Selected Posts')
