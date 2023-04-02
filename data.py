from main import site, db, Order, Product, ItemsInOrder
from sqlalchemy.sql import text
import pandas as pd
from datetime import datetime

def get_order_info():
    sql = """
        SELECT i_i_o.idOrder, i_i_o.idItem, P.title, P.price, P.img, O.date  
        FROM items_in_order i_i_o
        LEFT JOIN 'order' as O ON O.idOrder = i_i_o.idOrder
        INNER JOIN Product as P ON p.idItem = i_i_o.idItem
    """

    cursor = db.session.execute(text(sql))
    return cursor.all()


def history_order():



def get_data_history_user(path, user_id=0):
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

def insert_data_items_product(path='dataset/orders_v2.csv', user_id=0):
    history = get_data_history_user(path=path, user_id=user_id)

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
    #insert_data_items_product(path='dataset/orders_v2.csv', user_id=-1)
    insert_data_order(path='dataset/orders_v2.csv', user_id=-1)