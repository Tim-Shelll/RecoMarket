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

    firstname = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    lastname = StringField('Отчество')

    sex = SelectField('Пол', choices=['Мужской', 'Женский'])

    email = StringField('Электронная почта', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])

    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')


class CheckoutForm(FlaskForm):
    firstname = StringField('Имя', validators=[DataRequired()])

    phone = StringField('Телефон', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    street = StringField('Улица', validators=[DataRequired()])

    house = StringField('Дом', validators=[DataRequired()])
    apartment = StringField('Квартира', validators=[DataRequired()])
    entrance = StringField('Подъезд', validators=[DataRequired()])
    floor = StringField('Этаж', validators=[DataRequired()])

    submit = SubmitField('Совершить заказ')

