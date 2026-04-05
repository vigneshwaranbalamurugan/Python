import sqlite3

def get_connection():
    return sqlite3.connect("sales.db")

def fetch_sales(month):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT region, revenue, units, date
        FROM sales
        WHERE month = ?
        """,
        (month,)
    )

    data = cursor.fetchall()
    conn.close()

    return data