#region Import

from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm
from flask_login import logout_user, current_user, login_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from templates import ORDERS_TO_USER
from helpers import get_valid_order

#endregion


#region Application

__table_args__ = {'extend_existing': True}

site = Flask(__name__)
site.config['SECRET_KEY'] = "I'm Andrey"
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(site)

#endregion


#region Database

db = SQLAlchemy(site)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    login = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    photo = db.Column(db.String, default=None)
    created_on = db.Column(db.DateTime(), default=datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


class Product(db.Model):
    idItem = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String, nullable=False)


class Order(db.Model):
    idOrder = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    shopCode = db.Column(db.Integer, nullable=False)

    @staticmethod
    def select_data_order_to_user(user_id):
        sql = ORDERS_TO_USER.format(user_id=user_id)
        cursor = db.session.execute(text(sql))

        return cursor.all()


class ItemsInOrder(db.Model):
    idOrder = db.Column(db.Integer, primary_key=True, unique=False)
    idItem = db.Column(db.Integer, primary_key=True, unique=False)
    numItems = db.Column(db.Integer, nullable=False)


#endregion


#region Redirect

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))

@site.route('/logout')
def logout():
    logout_user()
    return redirect('index')


@site.route('/')
@site.route('/index')
def index():
    print(current_user)
    products = Product.query.order_by(Product.price).all()
    recomendations = Product.query.order_by(Product.img).limit(4)
    return render_template('index.html', products=products, recomendations=recomendations)


@site.route('/checkout')
def checkout():
    return render_template('cart.html')


@site.route('/history_orders/<int:user_id>')
def history_orders(user_id):
    purchases = Order.select_data_order_to_user(user_id)
    history = get_valid_order(purchases)

    return render_template('history.html', history=history)


@site.route('/history_orders')
def history_order():
    return render_template('history.html')


@site.route('/login', methods=['POST', 'GET'])
def signin():
    form = LoginForm()
    if not current_user.is_authenticated:
        form = LoginForm()
        if request.method == 'POST':
            user = User.query.filter_by(login=form.login.data).first()
            if user is None or not user.check_password(form.password.data):
                message = 'Invalid username or password'
                return render_template('login.html', message=message, form=form)

            login_user(user, remember=form.remember_me.data)
            return redirect('/index')

        return render_template('login.html', form=form)
    else:
        return redirect('/index')

    return render_template('login.html', form=form)



@site.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    """if not current_user.is_authenticated:
        form = RegistrationForm()
        message = ""
        if request.method == 'POST':
            return redirect('/index')

        return render_template('registration.html', form=form)
    else:
        return redirect('/index')"""
    return render_template('registration.html', form=form)
#endregion


if __name__ == "__main__":
    site.run(debug=True)

# Завтрашние задачи
# ✔ Отцентрировать изображения продуктов в карточках
# ️✔ Создать страничку сайта с историей покупок пользователя, чтобы была видна статистика ( история заказов, не товаров )
# ️✔ Автоматизировать работу базы данных по заполнению данными о товарах и рекоменддациях
# ️Разобраться с выгрузкой рекомендаций по модели