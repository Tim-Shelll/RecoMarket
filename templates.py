ORDERS_TO_USER = """
    SELECT * FROM (
        SELECT O.client, i_i_o.idOrder, i_i_o.idItem, P.title, O.date, P.price, P.img  
        FROM items_in_order i_i_o
        LEFT JOIN 'order' as O ON O.idOrder = i_i_o.idOrder
        INNER JOIN Product as P ON p.idItem = i_i_o.idItem
    ) t
    
    WHERE t.client = {user_id}
    ORDER BY 5 DESC
"""

PRODUCTS_IN_PROD_IDS = """
    SELECT * FROM product
    WHERE idItem in {prod_ids}
    ORDER BY 1
"""

DISTINCT_USERS = """
    SELECT COUNT(DISTINCT id) FROM user
"""

DISTINCT_PRODUCTS = """
    SELECT COUNT(*) FROM product
"""