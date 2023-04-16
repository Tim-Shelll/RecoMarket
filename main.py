import pandas as pd
from datetime import datetime
from flask import render_template, request, redirect
from flask_login import logout_user, current_user, login_user, LoginManager

from app import app, db, User, Product, Order, ItemsInOrder, ItemsInBag, Category
from forms import LoginForm, RegistrationForm
from helpers import get_valid_order, product_with_numItems, create_beautiful_history
from refactor_data import insert_dataset_data
from manipulation_data import orders_update, recomendations_all


#region Initializate

recs = pd.read_csv('dataset/recomendations.csv', sep=',')
login_manager = LoginManager()
login_manager.init_app(app)

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
    if current_user.is_authenticated:
        recs = pd.read_csv('dataset/recomendations.csv', sep=',')
        rec_cur_user = recs[recs.user_id == current_user.id]
        prod_ids = "(" + ", ".join([str(rec) for rec in rec_cur_user['prod_id'].values]) + ")"
        recomendations = Product.select_data_product_by_ids(prod_ids)

    else:
        recomendations = None

    return render_template('index.html', categories=categories, products=products, recomendations=recomendations)


@app.route('/index/<int:idItem>', methods=['POST', 'GET'])
def item(idItem):
    if request.method == 'POST':
        iteminbag = ItemsInBag.query.filter_by(idUser=current_user.id, idItem=idItem).first()
        if iteminbag:
            iteminbag.numItems += 1
        else:
            db.session.add(ItemsInBag(idUser=current_user.id, idItem=idItem, numItems=1))

        db.session.commit()

    return redirect('/')


@app.route('/profile')
def profile_current():
    if current_user.is_authenticated:
        user = User.query.get(int(current_user.id))
        return render_template('profile.html', user=user)
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

    return render_template('history.html', history=beautiful_history)


@app.route('/login', methods=['POST', 'GET'])
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


@app.route('/registration', methods=['POST', 'GET'])
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


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    if current_user.is_authenticated:
        if request.method == 'POST':
            itemsinbag = ItemsInBag.query.filter_by(idUser=current_user.id).all()
            if itemsinbag:
                orderId = insert_dataset_data(itemsinbag, current_user.id)
                orders_update(itemsinbag, orderId)


        items_in_cart = ItemsInBag.query.filter_by(idUser=current_user.id).all()
        prod_ids = "(" + ", ".join([str(item.idItem) for item in items_in_cart]) + ")"
        items_in_bag = Product.select_data_product_by_ids(prod_ids)
        iib_with_num = product_with_numItems(items_in_bag, (item.numItems for item in items_in_cart))

        return render_template('cart.html', items_in_bag_with_num=iib_with_num)
    else:
        return render_template('cart.html')

#endregion


#endregion

if __name__ == "__main__":
    app.run(host='192.168.1.43', port='8080' ,debug=True)
