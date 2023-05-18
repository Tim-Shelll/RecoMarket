from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):

    firstname = StringField('Имя')
    surname = StringField('Фамилия')
    lastname = StringField('Отчество')

    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):

    firstname = StringField('Имя')
    surname = StringField('Фамилия')
    lastname = StringField('Отчество')

    email = StringField('Электронная почта', validators=[DataRequired()])
    login = StringField('Логин')

    password = PasswordField('Пароль')
    password_repeat = PasswordField('Повторите пароль')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')
