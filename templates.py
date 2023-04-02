from main import db, site
from sqlalchemy.sql import text

ORDERS_TO_USER = """
    SELECT * FROM (
        SELECT O.client, i_i_o.idOrder, i_i_o.idItem, P.title, O.date, P.price, P.img  
        FROM items_in_order i_i_o
        LEFT JOIN 'order' as O ON O.idOrder = i_i_o.idOrder
        INNER JOIN Product as P ON p.idItem = i_i_o.idItem
    ) t
    
    WHERE t.client = {user_id}
"""

def query():
    sql = ORDERS_TO_USER.format(user_id=0)
    cursor = db.session.execute(text(sql))
    for row in cursor.fetchall():
        print(row)

with site.app_context():
    query()