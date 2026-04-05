import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "sales.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region TEXT,
        revenue REAL,
        units INTEGER,
        date TEXT,
        month TEXT
    )
    """)
    conn.commit()
    conn.close()

def generate_sales_data(month):
    regions = ["North", "South", "East", "West"]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    start_date = datetime.strptime(month + "-01", "%Y-%m-%d")
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        for region in regions:
            revenue = random.randint(5000, 20000)
            if region == "West":
                revenue = int(revenue * 0.75)

            units = random.randint(50, 200)
            cursor.execute("""
            INSERT INTO sales(region, revenue, units, date, month)
            VALUES (?, ?, ?, ?, ?)
            """, (
                region,
                revenue,
                units,
                current_date.strftime("%Y-%m-%d"),
                month
            ))
    conn.commit()
    conn.close()


def main():

    print("Creating table...")
    create_table()

    print("Seeding January 2026 data...")
    generate_sales_data("2026-01")

    print("Seeding December 2025 data...")
    generate_sales_data("2025-12")

    print("Dummy data inserted successfully")


if __name__ == "__main__":
    main()