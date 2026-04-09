from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import date
from database import create_table, insert_products
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Firefox/123.0",
    "Chrome/122.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Safari/537.36 Edg/122.0",
    "Chrome/120.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 Safari/537.36 Edg/120.0",
    "Chrome/118.0 (X11; Linux x86_64) AppleWebKit/537.36 Safari/537.36 Edg/118.0",
    "Chrome/122.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Safari/537.36 OPR/122.0",
]

def get_random_driver():

    options = Options()
    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={user_agent}")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_experimental_option("useAutomationExtension",False)

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service,options=options)
    return driver

def scrape_products():
    today = str(date.today())
    data = []
    for page in range(1, 6):
            url = f"https://www.amazon.in/s?k=laptop&page={page}"
            driver = get_random_driver()  
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