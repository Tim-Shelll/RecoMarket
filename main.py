#region Import

from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm
from flask_login import logout_user, current_user, login_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

from templates import ORDERS_TO_USER, PRODUCTS_IN_PROD_IDS
from helpers import get_valid_order, product_with_numItems, create_beautiful_history
from model import path

#endregion


#region Application

__table_args__ = {'extend_existing': True}

site = Flask(__name__)
site.config['SECRET_KEY'] = "I'm Andrey"
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(site)

recomends = pd.read_csv('dataset/recomendations.csv', sep=',')

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

    @staticmethod
    def select_data_product_by_ids(prod_ids):
        sql = PRODUCTS_IN_PROD_IDS.format(prod_ids=prod_ids)
        cursor = db.session.execute(text(sql))

        return cursor.all()


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


class ItemsInBag(db.Model):
    idUser = db.Column(db.Integer, primary_key=True, unique=False)
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
    products = Product.query.order_by(Product.idItem).all()
    if current_user.is_authenticated:
        rec_cur_user = recomends[recomends.user_id == current_user.id]
        recomendations = Product.select_data_product_by_ids(tuple(rec_cur_user['prod_id'].values))
    else:
        recomendations = None

    return render_template('index.html', products=products, recomendations=recomendations)


@site.route('/index/<int:idItem>', methods=['POST', 'GET'])
def item(idItem):
    print(idItem)
    iteminbag = ItemsInBag.query.filter_by(idUser=current_user.id, idItem=idItem).first()
    if iteminbag:
        iteminbag.numItems += 1
    else:
        db.session.add(ItemsInBag(idUser=current_user.id, idItem=idItem, numItems=1))

    db.session.commit()

    return redirect('/')


@site.route('/profile')
def profile_current():
    user = User.query.get(int(current_user.id))
    return render_template('profile.html', user=user)


@site.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)


@site.route('/history_orders/<int:user_id>')
def history_orders(user_id):
    purchases = Order.select_data_order_to_user(user_id)
    history = get_valid_order(purchases)
    beautiful_history = create_beautiful_history(history)

    return render_template('history.html', history=beautiful_history)


@site.route('/history_orders')
def history_order():
    purchases = Order.select_data_order_to_user(current_user.id)
    history = get_valid_order(purchases)
    beautiful_history = create_beautiful_history(history)
    print(beautiful_history)

    return render_template('history.html', history=beautiful_history)


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


@site.route('/cart', methods=['POST', 'GET'])
def bag():
    print(request.method == 'POST')
    if request.method == 'POST':
        itemsinbag = ItemsInBag.query.filter_by(idUser=current_user.id)
        if itemsinbag:
            insert_dataset_data(itemsinbag)

    if current_user.is_authenticated:
        items_in_cart = ItemsInBag.query.filter_by(idUser=current_user.id)
        prod_ids = "(" + ", ".join([str(item.idItem) for item in items_in_cart]) + ")"
        items_in_bag = Product.select_data_product_by_ids(prod_ids)
        iib_with_num = product_with_numItems(items_in_bag, (item.numItems for item in items_in_cart))

        return render_template('cart.html', items_in_bag_with_num=iib_with_num)
    else:
        return render_template('cart.html')

#endregion


#region BL

def insert_dataset_data(itemsinbag):
    datetime_now = str(datetime.now().date()) + ' ' + str(datetime.now().time()).split('.')[0]
    order = Order(
        client=current_user.id,
        date=datetime.strptime(datetime_now, "%Y-%m-%d %H:%M:%S"),
        shopCode=1
    )
    db.session.add(order)
    db.session.commit()

    for iteminbag in itemsinbag:
        iteminorder = ItemsInOrder(idOrder=order.idOrder, idItem=iteminbag.idItem, numItems=iteminbag.numItems)
        db.session.add(iteminorder)
        db.session.delete(iteminbag)

    db.session.commit()

#endregion

if __name__ == "__main__":
    site.run(host='192.168.1.43', port='8080' ,debug=True)
