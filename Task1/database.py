import sqlite3

def create_table():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        name TEXT,
        price TEXT,
        date TEXT,
        link TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_products(data):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?,?)",
     data
    )
    conn.commit()
    conn.close()