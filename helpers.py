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

    return orders


def refactor_img(path):
    img = cv2.imread(path)
    if  img is None:
        print('img is None')
    else:
        ref_img = cv2.resize(img, (img.shape[1] // 3 * 2, img.shape[0] // 3 * 2))
        cv2.imwrite(os.getcwd() + r'/static/users/andrey.jpg', ref_img)


def product_with_numItems(products, numItems):
    return [(product, numItem) for product, numItem in zip(products, numItems)]


history = {
    (438, '2022-01-03 16:22:30'): [
        (1, 438, 9, "Салат 'Крабовый'", '2022-01-03 16:22:30', 129, '/static/images/9.jpg'),
        (1, 438, 11, 'Сок (1 л.)', '2022-01-03 16:22:30', 149, '/static/images/11.jpg')
    ],
    (325, '2022-01-15 17:45:50'): [
        (1, 325, 1, 'Каша овсяная на молоке (250 гр.)', '2022-01-15 17:45:50', 49, '/static/images/1.jpeg'),
        (1, 325, 21, 'Блины с яйцом', '2022-01-15 17:45:50', 249, '/static/images/21.jpg'),
        (1, 325, 24, 'Блины с бананом', '2022-01-15 17:45:50', 279, '/static/images/24.jpg')
    ],
    (104, '2022-02-24 20:12:00'): [
        (1, 104, 3, 'Лапша куриная (0,5 л)', '2022-01-24 20:12:00', 69, '/static/images/3.jpg'),
        (1, 104, 16, 'Кофе латте (0,3 л.)', '2022-01-24 20:12:00', 199, '/static/images/16.jpg'),
        (1, 104, 17, 'Кофе капуччино (0,3 л.)', '2022-01-24 20:12:00', 209, '/static/images/17.jpg')
    ],
    (104, '2023-01-24 20:12:00'): [
        (1, 104, 3, 'Лапша куриная (0,5 л)', '2022-01-24 20:12:00', 69, '/static/images/3.jpg'),
        (1, 104, 16, 'Кофе латте (0,3 л.)', '2022-01-24 20:12:00', 199, '/static/images/16.jpg'),
        (1, 104, 17, 'Кофе капуччино (0,3 л.)', '2022-01-24 20:12:00', 209, '/static/images/17.jpg')
    ]
}


month = {
    1: 'Январь',    7: 'Июль',
    2: 'Февраль',   8: 'Август',
    3: 'Март',      9: 'Сентябрь',
    4: 'Апрель',    10: 'Октябрь',
    5: 'Май',       11: 'Ноябрь',
    6: 'Июнь',      12: 'Декабрь'
}


def get_valid_time(hour, minute):
    hour = hour if hour > 9 else "0" + str(hour)
    minute = minute if minute > 9 else "0" + str(minute)

    return "{}:{}".format(hour, minute)


def create_beautiful_history(history):

    beautiful_history = {} #list years

    for (order_id, date_time) in history.keys():
        cur_date = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        cur_date, cur_date_time = \
            (cur_date.date(), cur_date.time())

        if cur_date.year not in beautiful_history:
            beautiful_history[cur_date.year] = {} # list months

        months = beautiful_history[cur_date.year]
        if month[cur_date.month] not in months:
            months[month[cur_date.month]] = {} # list days

        days = months[month[cur_date.month]]
        if cur_date.day not in days:
            days[(cur_date.day, get_valid_time(cur_date_time.hour, cur_date_time.minute))] = [] # list months

        day = days[(cur_date.day, get_valid_time(cur_date_time.hour, cur_date_time.minute))]
        for order in history[(order_id, date_time)]:
            day.append(order)

    return beautiful_history


PATH = r'static\users\andrey.jpg'