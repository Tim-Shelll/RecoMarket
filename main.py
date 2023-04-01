from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

site = Flask(__name__)
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# site.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# site.config['MAIL_PORT'] = 587
# site.config['MAIL_USE_TLS'] = True
# site.config['MAIL_USERNAME'] = 'youmail@gmail.com'
# site.config['MAIL_DEFAULT_SENDER'] = 'youmail@gmail.com'
# site.config['MAIL_PASSWORD'] = 'password'

# manager = Manager(site)
# manager.add_command('db', MigrateCommand)
db = SQLAlchemy(site)
# migrate = Migrate(site, db)
# mail = Mail(site)
# login_manager = LoginManager(site)


class Product(db.Model):
    idItem = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String, nullable=False)


class Order(db.Model):
    idOrder = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Text, nullable=False)
    shopCode = db.Column(db.Integer, nullable=False)


class ItemsInOrder(db.Model):
    idItem = db.Column(db.Integer, primary_key=True)
    idOrder = db.Column(db.Integer, primary_key=True)
    numItems = db.Column(db.Integer, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    updated_on = db.Column(db.DateTime(), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


@site.route('/')
def index():
    items = Product.query.order_by(Product.price).all()
    recomendations = Product.query.order_by(Product.img).limit(4)
    return render_template('index.html', products=items, recomendations=recomendations)


@site.route('/checkout')
def checkout():
    return render_template('cart.html')


@site.route('/register')
def register():
    return render_template('register.html')


@site.route('/login')
def login():
    return render_template('login.html')


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
