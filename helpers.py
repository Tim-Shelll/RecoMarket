from constant import name_product, price_product
from main import db, Product, site


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

with site.app_context():
    insert_data_product(name_product)
