from constant import name_product, price_product
from main import db, Product, site
import pandas as pd


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


def insert_data_items_product(path='dataset/orders_v2.csv', user_id=0):
    history = history_order(path=path, user_id=user_id)

    for order_id in history.keys():
        for order in history[order_id]:
            itemsOrder = ItemsInOrder(
                idOrder=int(order_id),
                idItem=order[0],
                numItems=order[1]
            )

            db.session.add(itemsOrder)
            db.session.commit()


def insert_data_order(path='dataset/orders_v2.csv', user_id=-1):
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


with site.app_context():
    insert_data_product(name_product)
