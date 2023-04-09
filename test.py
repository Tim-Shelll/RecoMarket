import pandas as pd

data = pd.read_csv('dataset/orders_v2.csv')
data['rank_baseline'] = 11 - data['prod_id']

print(data)