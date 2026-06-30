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
