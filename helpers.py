name_product = [
    "Каша овсяная на молоке (250 гр.)", "Борщ со сметаной и зеленю (0,5 л)", "Лапша куриная (0,5 л)",
    "Кремовый суп с гренками (0,5 л)", "Суп томатный (0,5 л)",
    "Салат 'Цезарь'", "Салат 'Оливье'", "Салат 'Селёдка под шубой'", "Салат 'Крабовый'", "Салат из морепродуктов",
    "Сок (1 л.)", "Coca-Cola (1 л.)", "Sprite (1,5 л.)", "Черноголовка (1,5 л.)", "Очаковский квас (1,5 л.)",
    "Кофе латте (0,3 л.)", "Кофе капуччино (0,3 л.)", "Горячий шоколад (0,3 л)", "Раф малиновый (0,3 л)",
    "Чай малиновый (0,3 л)",
    "Блины с яйцом", "Блины с мясом", "Блины с яйцом и ветчиной и сыром", "Блины с бананом", "Блины с яблоком"
]

images = [
    "https://montisbar.ru/wp-content/uploads/2/d/9/2d9481b933c01fa8dc001774350901c0.jpeg"
]

price_product = [49 + 10 * inc for inc in range(len(name_product))]

from main import db, Product


def insert_data_product(data_product):
    for id in range(len(data_product)):
        sql = """
            INSERT INTO Product('title', 'desc', 'price', 'img') 
            VALUES ({}, {}, {}, {})
            """.format(data_product[id], "", price_product[id], images[0])
        db.session.execute(sql)

        db.session.commit()


insert_data_product(name_product)
