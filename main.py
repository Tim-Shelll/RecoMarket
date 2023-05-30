import socket
import pandas as pd

from flask import render_template, request, redirect, jsonify
from flask_login import logout_user, current_user, login_user, LoginManager

from app import app, db, User, Product, Order, ItemsInBag, Category, ItemsInFavorite
from forms import LoginForm, RegistrationForm
from helpers import get_valid_order, product_with_numItems, create_beautiful_history
from refactor_data import insert_dataset_data
from manipulation_data import orders_update, recomendations_all


#region Initializate

login_manager = LoginManager()
login_manager.init_app(app)

host = socket.gethostbyname(socket.gethostname())
port = '8080'

def cart_and_like():
    cart = ItemsInBag.query.filter_by(idUser=current_user.id).all()
    like = ItemsInFavorite.query.filter_by(idUser=current_user.id).all()
    return cart, like


#endregion


#region Redirect

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))


@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')


@app.route('/')
@app.route('/index')
def index():
    products = Product.query.order_by(Product.idItem).all()
    categories = Category.query.all()
    products_sales = Product.select_best_sales_products()

    if current_user.is_authenticated:

        recs = pd.read_csv('dataset/recomendations.csv', sep=',')

        rec_cur_user = recs[recs.user_id == current_user.id]
        prod_ids = "(" + ", ".join([str(rec) for rec in rec_cur_user['prod_id'].values]) + ")"
        recomendations = Product.select_data_product_by_ids(prod_ids)

        cart, like = cart_and_like()
        items_favorite = [item.idItem for item in like]

    else:
        recomendations, cart, like, items_favorite = None, [], [], []

    return render_template('index.html', categories=categories, products=products,
                                         recomendations=recomendations, cart=len(cart), like=len(like),
                                         items_favorite=items_favorite, products_sales=products_sales)


@app.route('/index/<int:idItem>', methods=['POST', 'GET'])
def item(idItem):
    if request.method == 'POST':
        iteminbag = ItemsInBag.query.filter_by(idUser=current_user.id, idItem=idItem).first()
        if iteminbag:
            iteminbag.numItems += 1
        else:
            db.session.add(ItemsInBag(idUser=current_user.id, idItem=idItem, numItems=1))

        db.session.commit()

        quantity = len(ItemsInBag.get_count_products(current_user.id))

    return jsonify({'quantity': quantity})


@app.route('/profile')
def profile_current():
    if current_user.is_authenticated:
        user = User.query.get(int(current_user.id))
        cart, like = cart_and_like()

        return render_template('profile.html', user=user, cart=len(cart), like=len(like))
    else:
        return redirect('/')


@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)


@app.route('/history_orders/<int:user_id>')
def history_orders(user_id):
    purchases = Order.select_data_order_to_user(user_id)
    history = get_valid_order(purchases)
    beautiful_history = create_beautiful_history(history)

    return render_template('history.html', history=beautiful_history)


@app.route('/history_orders')
def history_order():
    purchases = Order.select_data_order_to_user(current_user.id)
    history = get_valid_order(purchases)
    beautiful_history = create_beautiful_history(history)
    cart, like = cart_and_like()

    return render_template('history.html', history=beautiful_history, cart=len(cart), like=len(like))


@app.route('/login', methods=['POST', 'GET'])
def signin():

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


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if not current_user.is_authenticated:
        form = RegistrationForm()
        if request.method == 'POST':
            user = User()
            user.username = " ".join([form.surname.data, form.firstname.data, form.lastname.data])
            user.login = form.login.data
            user.email = form.email.data
            user.photo = '/static/users/avatar-{}.png'.format('man' if form.sex.data == 'Мужской' else 'woman')
            user.set_password(form.password.data)

            if form.password.data == form.password_repeat.data:
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)

                return redirect('/index')

            else:
                message = 'Invalid data enviroment'
                return render_template('registration.html', message=message, form=form)

        return render_template('registration.html', form=form)
    else:
        return redirect('/index')

    return render_template('registration.html', form=form)


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    if current_user.is_authenticated:
        if request.method == 'POST':
            itemsinbag = ItemsInBag.query.filter_by(idUser=current_user.id).all()
            if itemsinbag:
                orderId = insert_dataset_data(itemsinbag, current_user.id)
                orders_update(itemsinbag, orderId)

                recomendations_all()

        items_in_cart = ItemsInBag.query.filter_by(idUser=current_user.id).all()
        prod_ids = "(" + ", ".join([str(item.idItem) for item in items_in_cart]) + ")"
        items_in_bag = Product.select_data_product_by_ids(prod_ids)
        iib_with_num = product_with_numItems(items_in_bag, (item.numItems for item in items_in_cart))

        cart, like = cart_and_like()

        return render_template('cart.html', items_in_bag_with_num=iib_with_num, cart=len(cart), like=len(like))
    else:
        return render_template('cart.html')


@app.route('/cart/<int:idItem>', methods=['POST', 'GET'])
def action_cart(idItem):
    if request.method == 'POST':
        itemsinbag = ItemsInBag.query.filter_by(idUser=current_user.id, idItem=idItem).first()
        change = int(request.values['change'])
        itemsinbag.numItems += change
        if not itemsinbag.numItems:
            db.session.delete(itemsinbag)

        db.session.commit()

    return jsonify({idItem: itemsinbag.numItems})


@app.route('/likes')
def likes():
    if current_user.is_authenticated:
        prod_ids = [str(item.idItem) for item in ItemsInFavorite.get_count_products(idUser=current_user.id)]
        favorites = Product.select_data_product_by_ids(prod_ids="(" + ", ".join(prod_ids) + ")")
        cart = len(ItemsInBag.get_count_products(current_user.id))

        return render_template('favorite.html', favorites=favorites, like=len(prod_ids), cart=cart)
    else:
        return render_template('favorite.html')


@app.route('/likes/<int:idItem>', methods=['POST', 'GET'])
def like(idItem):
    if request.method == 'POST':
        items_in_favorite = ItemsInFavorite.query.filter_by(idUser=current_user.id, idItem=idItem).all()
        if not items_in_favorite:
            db.session.add(ItemsInFavorite(idUser=current_user.id, idItem=idItem))
            db.session.commit()

        recomendations_all()

        like = len(ItemsInFavorite.get_count_products(current_user.id))

    return jsonify({'like': like})


@app.route('/likes/delete', methods=['POST', 'GET'])
def likes_delete():
    if request.method == 'POST':
        idItem = int(request.values['idItem'])
        items_in_favorite = ItemsInFavorite.query.filter_by(idUser=current_user.id, idItem=idItem).first()
        db.session.delete(items_in_favorite)
        db.session.commit()

    prod_ids = [str(item.idItem) for item in ItemsInFavorite.get_count_products(idUser=current_user.id)]

    return jsonify({'likes': len(prod_ids)})


@app.route('/delete/item', methods=['POST', 'GET'])
def cart_delete():
    if request.method == 'POST':
        items_in_bag = ItemsInBag.query.filter_by(idUser=current_user.id, idItem=int(request.values['idItem'])).first()
        db.session.delete(items_in_bag)
        db.session.commit()

    items_in_cart = ItemsInBag.query.filter_by(idUser=current_user.id).all()

    return jsonify({'quantity': len(items_in_cart)})

#endregion


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
