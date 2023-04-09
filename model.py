import pandas as pd
from scipy import sparse
from sklearn.model_selection import train_test_split, cross_validate
from lightfm import cross_validation, LightFM

path = 'dataset/orders_v2.csv'
n_user = 5


def validate_data(path):
    orders = pd.read_csv(path, sep=',')

    orders_purch = orders.groupby(['user_id', 'prod_id'])['cat_id'].count().reset_index()
    orders_purch.columns = ['user_id', 'prod_id', 'purchase']
    orders_purch_sort = orders_purch.sort_values(['user_id', 'purchase'], ascending=False).copy()

    return orders_purch_sort


def set_rank_product(orders_purch_sort):
    orders_purch_sort_data = orders_purch_sort.values
    user_id = orders_purch_sort_data[0][0]
    prod_id = orders_purch_sort_data[0][1]
    bays = orders_purch_sort_data[0][2]

    n = 1
    count_bay = []
    count_bay.append(n)
    for row in orders_purch_sort_data[1:]:
      if (row[0] == user_id):
        n += 1
        user_id = row[0]
        prod_id = row[1]
        bays = row[2]
        count_bay.append(n)
      else:
        n = 1
        user_id = row[0]
        prod_id = row[1]
        bays = row[2]
        count_bay.append(n)

    orders_purch_sort.loc[:, 'rank'] = count_bay
    orders_purch_sort = orders_purch_sort[orders_purch_sort['rank'] < 11]
    orders_purch_sort['rank_baseline'] = 11 - orders_purch_sort['rank']

    return orders_purch_sort


def split_data(orders_purch_sort):
    # Коэффициент разбиения примем равный 0.8

    orders_train, orders_test = train_test_split(orders_purch_sort, train_size=.8)
    return orders_train, orders_test


def create_pivot_table(orders_train):
    orders_train_pivot = orders_train.pivot_table(
        index='user_id',
        values='rank_baseline',
        columns='prod_id',
        aggfunc={'rank_baseline': 'mean'},
        margins=True,
        fill_value=0
    )

    data_pivot = orders_train_pivot.reset_index()
    train_pivot_np = data_pivot.to_numpy()
    data_ds = train_pivot_np[:-1, 1:-1].astype('int')
    sData = sparse.csr_matrix(data_ds)
    orders_train_pivot, orders_test_pivot = cross_validation.random_train_test_split(
        sData,
        test_percentage=0.2,
        random_state=None
    )

    return sData, orders_train_pivot, orders_test_pivot


def model(orders_train_pivot):
    # В качестве функции потерь были предложены следующие:
    # "logistic", "warp", "bpr", "warp-kos"
    # Выберем "warp"

    model_LightFM = LightFM(loss='warp')
    model_LightFM.fit(orders_train_pivot, epochs=1000, num_threads=2)

    return model_LightFM


def recomendations(model_LightFM, sData):
    pred = model_LightFM.predict_rank(sData)
    ar = pred.toarray()
    predict = []
    timer_ids = range(n_user)
    prod_ids = range(100)

    for i in range(ar.shape[0]):
        for m in range(ar.shape[1]):
            ar_list = []
            if ar[i, m] > 0 and ar[i, m] < 11:
                ar_list.append(timer_ids[i])
                ar_list.append(prod_ids[m])
                ar_list.append(ar[i, m])
                predict.append(ar_list)
    predict_df = pd.DataFrame(predict, columns=['user_id', 'prod_id', 'pred_rang'])

    recom_users = {i: [] for i in range(n_user)}

    for user_id, product_id, rank in predict_df.values:
        if len(recom_users[user_id]) < 5:
            recom_users[user_id].append({product_id: rank})

    return recom_users


orders_purch_sort = validate_data(path)
orders_purch_sort = set_rank_product(orders_purch_sort)
orders_train, orders_test = split_data(orders_purch_sort)
sData, orders_train_pivot, orders_test_pivot = create_pivot_table(orders_train)
model_LightFM = model(orders_train_pivot)
recom_users = recomendations(model_LightFM, sData)
print(recom_users)