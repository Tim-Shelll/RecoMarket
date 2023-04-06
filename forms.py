from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):

    firstname = StringField('Firstname')
    surname = StringField('Surname')
    lastname = StringField('Lastname')

    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):

    firstname = StringField('Firstname')
    surname = StringField('Surname')
    lastname = StringField('Lastname')

    email = StringField('Email', validators=[DataRequired()])
    login = StringField('Login')

    password = PasswordField('Password')
    password_repeat = PasswordField('Repeat Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Registry')
