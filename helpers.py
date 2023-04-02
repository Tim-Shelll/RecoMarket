from sqlalchemy.sql import text
from templates import ORDERS_TO_USER

def get_valid_order(purchases):
    orders = {}
    for purchase in purchases:
        if (purchase[1], purchase[4]) not in orders:
            orders[(purchase[1], purchase[4])] = [purchase]
        else:
            orders[(purchase[1], purchase[4])].append(purchase)

    return orders
