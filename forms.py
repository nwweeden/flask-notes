from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email
# import email_validator
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    '''form to register a new user'''

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    # email = StringField('Email', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class LoginForm(FlaskForm):
    '''form to log in'''

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])