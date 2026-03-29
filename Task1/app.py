from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import date
from database import create_table, insert_products

def scrape_products():
    today = str(date.today())

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    data = []
    for page in range(1, 6):
            url = f"https://www.amazon.in/s?k=laptop&page={page}"
            driver.get(url)
            time.sleep(5)
            products = driver.find_elements(
                By.XPATH,
                "//div[@data-component-type='s-search-result']"
            )
            print(f"Scraping page {page}...")
            for product in products:
                try:
                    name = product.find_element(By.TAG_NAME, "h2").text
                except:
                    name = "N/A"

                try:
                    price = product.find_element(
                        By.CLASS_NAME,
                        "a-price-whole"
                    ).text
                except:
                    price = "N/A"

                try:
                    link = product.find_element(
                        By.TAG_NAME,
                        "a"
                    ).get_attribute("href")
                except:
                    link = "N/A"

                data.append((name, price, today, link))

    driver.quit()
    return data

create_table()
products = scrape_products()
insert_products(products)

df = pd.DataFrame(
    products,
    columns=["Product Name", "Price", "Date","Link"]
)
today = str(date.today())

df.to_csv(f"{today}-products.csv", index=False)