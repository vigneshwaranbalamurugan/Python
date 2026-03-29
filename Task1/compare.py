import sqlite3
import pandas as pd
from datetime import date, timedelta

def compare_prices():
    conn = sqlite3.connect("products.db")
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    today_data = df[df["date"] == today]
    yesterday_data = df[df["date"] == yesterday]
    merged = pd.merge(today_data, yesterday_data, on="name")
    merged["price_x"] = merged["price_x"].astype(str).str.replace("₹", "").str.replace(",", "")
    merged["price_y"] = merged["price_y"].astype(str).str.replace("₹", "").str.replace(",", "")
    merged["price_x"] = pd.to_numeric(merged["price_x"], errors="coerce")
    merged["price_y"] = pd.to_numeric(merged["price_y"], errors="coerce")
    merged["change"] = merged["price_x"] - merged["price_y"]
    changes = merged[merged["change"] != 0]

    if len(changes) > 0:
        print("Price changes found:\n")
        for i, row in changes.iterrows():
            if row["change"] > 0:
                print(row["name"], "price increased 📈")
            else:
                print(row["name"], "price decreased 📉")
            print("Yesterday:", row["price_y"])
            print("Today:", row["price_x"])
            print("----------")

        changes.to_csv("price_changes.csv", index=False)
        print("Saved as price_changes.csv ✅")
    else:
        print("No price changes found")

compare_prices()