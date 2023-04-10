from constant import name_product, price_product, user_data, passwords
from main import db, Product, site, ItemsInOrder, Order, User
import pandas as pd


def get_data_history_user(path, user_id):
    orders = pd.read_csv(path, sep=',')
    orders_lst = {}
    # order_id, product_item, num_items, date, shop_code
    orders_user_id = orders[orders.user_id == user_id] if user_id != -1 else orders.copy()
    for order_id in orders_user_id.order_id.unique():
        current_order = orders_user_id[orders_user_id.order_id == order_id]
        current_order_values = current_order.values
        orders_lst[order_id] = [
            [
                c_o_v[-3],
                c_o_v[-1],
                c_o_v[6],
                c_o_v[1],
                c_o_v[2],
                c_o_v[5]
            ] for c_o_v in current_order_values
        ]

    return orders_lst


def insert_data_product(data_product):
    for id in range(len(data_product)):
        product = Product(
            title=name_product[id],
            desc="",
            price=price_product[id],
            img="/static/images/{}.jpg".format(id+1)
        )

        db.session.add(product)
        db.session.commit()


def insert_data_items_product(path, user_id):
    history = get_data_history_user(path=path, user_id=user_id)

    for order_id in history.keys():
        for order in history[order_id]:
            itemsOrder = ItemsInOrder(idOrder=int(order_id), idItem=order[0], numItems=order[1])

            row = (int(order_id), order[0], order[1])
            rows = ItemsInOrder.query.filter_by(idOrder=row[0], idItem=row[1]).first()
            if rows is not None:
                rows.numItems += row[2]
            else:
                db.session.add(itemsOrder)

            db.session.commit()


def insert_data_order(path):
    orders = pd.read_csv(path, sep=',')

    columns = ['order_id', 'user_id', 'date', 'time', 'shop']
    orders = orders[columns].drop_duplicates()
    for order_values in orders.values:
        order = Order(
            idOrder=order_values[0],
            client=order_values[1],
            date=order_values[2] + " " + order_values[3],
            shopCode=order_values[4]
        )

        db.session.add(order)
        db.session.commit()


def insert_data_user(path):

    users = []
    for id in range(len(user_data)):
        user = User()
        user.id = id
        user.username = user_data[id][0]
        user.email = user_data[id][1]
        user.login = user_data[id][2]
        user.set_password(passwords[id])
        user.photo = '/static/users/andrey.jpg'

        users.append(user)

    db.session.add_all(users)
    db.session.commit()


def insert_data_all_table(path, user_id):
    insert_data_product(name_product)
    print('Insert data product table complited')
    insert_data_user(path=path)
    print('Insert data user table complited')
    insert_data_order(path=path)
    print('Insert data order table complited')
    insert_data_items_product(path=path, user_id=-1)
    print('Insert data items_product complited')


path_to_orders = 'dataset/orders_v2.csv'

with site.app_context():
    insert_data_all_table(path=path_to_orders, user_id=-1)
    print('Insert data all tables complited')