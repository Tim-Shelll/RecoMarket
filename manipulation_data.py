import pandas as pd
from scipy import sparse
from sklearn.model_selection import train_test_split, cross_validate
from lightfm import cross_validation
from datetime import datetime

from model import model_LightFM
from app import app, User, Product, Order, ItemsInFavorite
from constant import price_product

path = 'dataset/orders_v2.csv'

#region manipulationData

def orders_update(itemsinbag, orderId):

    orders = pd.read_csv(path, sep=',')

    for iteminbag in itemsinbag:

        with app.app_context():
            order = Order.query.filter_by(idOrder=orderId).first()

        cur_date = datetime.strptime(order.date, "%Y-%m-%d %H:%M:%S")

        order = pd.DataFrame({
            "date": [cur_date.date()],
            "time": [cur_date.time()],
            "month": [cur_date.date().month],
            "week_day": [datetime.weekday(cur_date)],
            "shop": [1],
            "user_id": [iteminbag.idUser],
            "order_id": [orderId],
            "cat_id": [iteminbag.idItem // 5 + (0 if iteminbag.idItem % 5 == 0 else 1)],
            "prod_id": [iteminbag.idItem],
            "price": [price_product[iteminbag.idItem-1]],
            "cnt_prod": [iteminbag.numItems]
        })

        orders = orders.append(order, ignore_index=True)

    orders.to_csv('dataset/orders_v2.csv', index=False)


def validate_data(path):
    orders = pd.read_csv(path, sep=',')

    orders_purch = orders.groupby(['user_id', 'prod_id'])['cat_id'].count().reset_index()
    orders_purch.columns = ['user_id', 'prod_id', 'purchase']
    orders_purch_sort = orders_purch.sort_values(['user_id', 'purchase'], ascending=False).copy()

    return orders_purch_sort


def personal_favorite(personal, favorites):
    person_favorite = {}

    for favorite in favorites:
        if favorite.idUser in person_favorite:
            person_favorite[favorite.idUser].append(favorite.idItem)
        else:
            person_favorite[favorite.idUser] = [favorite.idItem]

    for user_id in person_favorite.keys():
        for prod_id in person_favorite[user_id]:
            current_p = personal[(personal.user_id == user_id) & (personal.prod_id == prod_id - 1)]
            if not len(current_p):
                psnl = pd.DataFrame({'user_id': [user_id], 'prod_id': [prod_id], 'purchase': [0], 'rank': [10]})
                personal = personal.append(psnl, ignore_index=True)
            else:
                current_p.values[0][3] = 10
                personal[(personal.user_id == user_id) & (personal.prod_id == prod_id - 1)] = current_p.values

    return personal, person_favorite


def set_rank_product(orders_purch_sort: pd.DataFrame, favorites):
    orders_purch_sort_data = orders_purch_sort.values
    user_id = orders_purch_sort_data[0][0]

    n = 1
    count_bay = [n]
    for row in orders_purch_sort_data[1:]:
        if (row[0] == user_id):
            n += 1
        else:
            n = 1

        user_id = row[0]
        count_bay.append(n)

    orders_purch_sort.loc[:, 'rank'] = count_bay
    orders_purch_sort, favorites = personal_favorite(orders_purch_sort, favorites)
    orders_purch_sort = orders_purch_sort[orders_purch_sort['rank'] < 11]
    orders_purch_sort['rank_baseline'] = 11 - orders_purch_sort['rank']

    return orders_purch_sort, favorites


def split_data(orders_purch_sort):

    # Коэффициент разбиения примем равный 0.8
    orders_train, orders_test = train_test_split(orders_purch_sort, train_size=.8)
    return orders_train, orders_test


def create_pivot_table(orders_train):
    # Составление таблицы пользователь - товар
    orders_train_pivot = orders_train.pivot_table(
        index='user_id',  # Ряды
        values='rank_baseline',  # Ранг товара на пересечении
        columns='prod_id',  # Колонки
        aggfunc={'rank_baseline': 'mean'},
        margins=True,
        fill_value=0
    )

    data_pivot = orders_train_pivot.reset_index() # Убираем индексы
    train_pivot_np = data_pivot.to_numpy() # Превращаем в numpy массив
    data_ds = train_pivot_np[:-1, 1:-1].astype('int')  # Валидация данных~
    sData = sparse.csr_matrix(data_ds) # Спарженная матрица
    orders_train_pivot, orders_test_pivot = cross_validation.random_train_test_split(
        sData,
        test_percentage=0.2, # Отношение 80% к 20%
        random_state=None
    )

    return sData, orders_train_pivot, orders_test_pivot


def recomendations(model_LightFM, sData, n_user, n_product):
    pred = model_LightFM.predict_rank(sData)
    ar = pred.toarray()
    predict = []
    user_ids = range(1, n_user + 1)
    prod_ids = range(1, n_product + 1)

    for i in range(len(user_ids)):
        for m in range(ar.shape[1]):
            ar_list = []
            if ar[i, m] > 0:
                ar_list.append(user_ids[i])
                ar_list.append(prod_ids[m])
                ar_list.append(ar[i, m])
                predict.append(ar_list)

    predict_df = pd.DataFrame(predict, columns=['user_id', 'prod_id', 'pred_rang'])

    recom_users = {i: [] for i in user_ids}

    for user_id, product_id, rank in predict_df.values:
        recom_users[user_id].append((product_id, rank))

    return recom_users


def convert_data_to_tuple(rec_users):
    recs = []

    for user_id in rec_users.keys():
        for row in rec_users[user_id]:
            recs.append([user_id, row[0]])

    return recs


def validate_recomendations(rec_users, favorites):
    for user, prod_ids in rec_users.items():
        prod_ids = sorted(prod_ids, key=lambda _ : _[1])

        favorite = reversed(favorites.get(user, []))

        prod_ids_validate = []
        for prod_id in prod_ids:
            if prod_id[0] in favorite:
                prod_ids_validate.append(prod_id)

        for prod_id in prod_ids:
            if prod_id[0] not in favorite:
                prod_ids_validate.append(prod_id)

        rec_users[user] = prod_ids_validate

    return rec_users


#endregion

def recomendations_all():
    with app.app_context(): # Получение данных с БД
        n_user = User.select_distinct_users()[0]
        n_product = Product.select_distinct_products()[0]
        favorites = ItemsInFavorite.query.all()

    orders_purch_sort = validate_data(path) # Валидация данных заказов пользователей
    orders_purch_sort, favorites = set_rank_product(orders_purch_sort, favorites) # Ранжирование товаров
    orders_train, orders_test = split_data(orders_purch_sort) # Разделение на трен. и тест. выборку
    sData, orders_train_pivot, orders_test_pivot = create_pivot_table(orders_train) # Смежная таблица

    rec_users = recomendations(model_LightFM, sData, n_user, n_product) # Прогноз рекомендаций
    #rec_users = validate_recomendations(rec_users, favorites) # Акцент на понравившиеся товары
    recoms = pd.DataFrame(columns=['user_id', 'prod_id'], data=convert_data_to_tuple(rec_users))

    recoms.to_csv('dataset/recomendations.csv') # Загрузка рекомендаций в датасет
