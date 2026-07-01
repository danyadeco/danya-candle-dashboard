import sqlite3
#====================================
# DATABASE CREATION
#====================================
def create_database():
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        sale_price REAL,
        cost_price REAL,
        stock INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    sale_date TEXT
    )
    """)
    connection.commit()
    connection.close()
#====================================
# PRODUCT FUNCTIONS
#====================================

def add_product(name, sale_price, cost_price, stock):
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO products
    (name, sale_price, cost_price, stock)
    VALUES (?, ?, ?, ?)
    """, (name, sale_price, cost_price, stock))

    connection.commit()
    connection.close()



def get_products():
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, name, sale_price, cost_price, stock
    FROM products
    """)

    products = cursor.fetchall()

    connection.close()

    return products

def delete_product(product_id):
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute(
        """DELETE FROM products WHERE id = ?""",
        (product_id,)
    )

    connection.commit()
    connection.close()

def update_product(product_id, sale_price, cost_price, stock):
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    UPDATE products
    SET sale_price = ?,
        cost_price = ?,
        stock = ?
    WHERE id = ?
    """, (
        sale_price,
        cost_price,
        stock,
        product_id
    ))

    connection.commit()
    connection.close()
#====================================
# SALE FUNCTIONS
#====================================

def add_sale(product_id, quantity, sale_date):
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO sales
    (product_id, quantity, sale_date)
    VALUES (?, ?, ?)
    """, (
        product_id,
        quantity,
        sale_date
    ))

    connection.commit()
    connection.close()

create_database()

def decrease_stock(product_id, quantity):
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    UPDATE products
    SET stock = stock - ?
    WHERE id = ?
    """, (
        quantity,
        product_id
    ))

    connection.commit()
    connection.close()
#=======================================
# GET SALES
#=======================================

def get_sales():
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, product_id, quantity, sale_date
    FROM sales
    """)

    sales = cursor.fetchall()

    connection.close()

    return sales


def get_sales_details():

    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        products.name,
        products.sale_price,
        products.cost_price,
        sales.quantity
    FROM sales
    JOIN products
    ON sales.product_id = products.id
    """)

    data = cursor.fetchall()

    connection.close()

    return data
#=================================
# BEST SELLER
#=================================

def get_best_seller():
    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        products.name,
        SUM(sales.quantity) as total_sold
    FROM sales
    JOIN products
    ON sales.product_id = products.id
    GROUP BY products.name
    ORDER BY total_sold DESC
    LIMIT 1
    """)

    best_seller = cursor.fetchone()

    connection.close()

    return best_seller
#=======================================
# SALES CHART DATA
#=======================================

def get_sales_chart_data():

    connection = sqlite3.connect("candles.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        products.name,
        SUM(sales.quantity)
    FROM sales
    JOIN products
    ON sales.product_id = products.id
    GROUP BY products.name
    ORDER BY SUM(sales.quantity) DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


