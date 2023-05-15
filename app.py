from flask import Flask
from flask_login import  UserMixin
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timezone
from templates import ORDERS_TO_USER, PRODUCTS_IN_PROD_IDS, DISTINCT_USERS, DISTINCT_PRODUCTS

from werkzeug.security import generate_password_hash, check_password_hash

__table_args__ = {'extend_existing': True}

app = Flask(__name__)
app.config['SECRET_KEY'] = "I'm Andrey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

    @staticmethod
    def select_distinct_users():
        return db.session.execute(text(DISTINCT_USERS)).first()

    def __repr__(self):
        return "<{}:{}:{}:{}>".format(self.id, self.username, self.email, self.login)


class Product(db.Model):
    idItem = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String, nullable=False)
    idCategory = db.Column(db.Integer, nullable=False)

    @staticmethod
    def select_data_product_by_ids(prod_ids):
        sql = PRODUCTS_IN_PROD_IDS.format(prod_ids=prod_ids)
        cursor = db.session.execute(text(sql))

        return cursor.all()

    @staticmethod
    def select_distinct_products():
        return db.session.execute(text(DISTINCT_PRODUCTS)).first()


class Category(db.Model):
    idCategory = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


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

    @staticmethod
    def get_count_products(idUser):
        return ItemsInBag.query.filter_by(idUser=idUser).all()


    def __repr__(self):
        return "<{}:{}:{}>".format(self.idUser, self.idItem, self.numItems)


class ItemsInLikes(db.Model):
    idOrder = db.Column(db.Integer, primary_key=True, unique=False)
    idItem = db.Column(db.Integer, primary_key=True, unique=False)