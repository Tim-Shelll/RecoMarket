import cv2
import os
import datetime


def get_valid_order(purchases):
    orders = {}

    for purchase in purchases:
        if (purchase[1], purchase[4]) not in orders:
            orders[(purchase[1], purchase[4])] = [purchase]
        else:
            orders[(purchase[1], purchase[4])].append(purchase)

    for order in list(orders.keys()):
        orders[(*order, sum([item[-1] * item[-3] for item in orders[order]]))] = orders[order]
        orders.pop(order)

    return orders


def product_with_numItems(products, numItems):
    return [(product, numItem) for product, numItem in zip(products, numItems)]



month = {
    1: 'января',    7: 'июля',
    2: 'февраля',   8: 'августа',
    3: 'марта',     9: 'сентября',
    4: 'апреля',    10: 'октября',
    5: 'мая',       11: 'ноября',
    6: 'июня',      12: 'декабря'
}


def get_valid_time(hour, minute):
    hour = hour if hour > 9 else "0" + str(hour)
    minute = minute if minute > 9 else "0" + str(minute)

    return "{}:{}".format(hour, minute)


def create_beautiful_history(history):

    beautiful_history = {} #icons years

    for (order_id, date_time, amount) in history.keys():
        cur_date = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        cur_date, cur_date_time = \
            (cur_date.date(), cur_date.time())

        if cur_date.year not in beautiful_history:
            beautiful_history[cur_date.year] = {} # icons months

        months = beautiful_history[cur_date.year]
        if month[cur_date.month] not in months:
            months[month[cur_date.month]] = {} # icons days

        days = months[month[cur_date.month]]
        if cur_date.day not in days:
            days[(cur_date.day, get_valid_time(cur_date_time.hour, cur_date_time.minute), amount)] = [] # icons months

        day = days[(cur_date.day, get_valid_time(cur_date_time.hour, cur_date_time.minute), amount)]
        for order in history[(order_id, date_time, amount)]:
            day.append(order)

    return beautiful_history


PATH = r'static\users\andrey.jpg'