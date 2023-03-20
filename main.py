from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

site = Flask(__name__)
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(site)


class Product(db.Model):
    idItem = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    Desc = db.Column(db.String(200), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    # Img = ссылка
    
    
class Order(db.Model):
    idOrder = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Text, nullable=False)
    shopCode = db.Column(db.Integer, nullable=False)


class ItemsInOrder(db.Model):
    idItem = db.Column(db.Integer, primary_key=True)
    idOrder = db.Column(db.Integer, primary_key=True)
    numItems = db.Column(db.Integer, nullable=False)


@site.route('/')
def index():
    return render_template('index.html')


@site.route('/checkout')
def checkout():
    return render_template('checkout.html')


if __name__ == "__main__":
    site.run(debug=True)
