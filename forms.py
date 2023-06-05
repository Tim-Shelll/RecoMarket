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

    sex = SelectField('Пол', choices=['Мужской', 'Женский'])

    email = StringField('Электронная почта', validators=[DataRequired()])
    login = StringField('Логин')

    password = PasswordField('Пароль')
    password_repeat = PasswordField('Повторите пароль')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')


class CheckoutForm(FlaskForm):
    firstname = StringField('Имя')

    phone = StringField('Телефон')
    city = StringField('Город')
    street = StringField('Улица')

    house = StringField('Дом')
    apartment = StringField('Квартира')
    entrance = StringField('Подъезд')
    floor = StringField('Этаж')

    submit = SubmitField('Совершить заказ')

