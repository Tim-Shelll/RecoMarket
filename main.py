from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

site = Flask(__name__)
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(site)


class Product(db.Model):
    idItem = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)


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
    items = Product.query.order_by(Product.price).all()
    return render_template('index.html', data=items)


@site.route('/checkout')
def checkout():
    return render_template('checkout.html')


@site.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Product(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template('create.html')


if __name__ == "__main__":
    site.run(debug=True)
