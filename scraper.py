import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

URL = "https://www.ebay.com/globaldeals/tech"
FILE_NAME = "ebay_tech_deals.csv"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(URL)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".dne-itemtile"))
)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.body.scrollHeight") > last_height
        )
        last_height = driver.execute_script("return document.body.scrollHeight")
    except TimeoutException:
        # No additional content loaded; assume we've reached the bottom
        break

products = driver.find_elements(By.CSS_SELECTOR, ".dne-itemtile")

data = []

for product in products:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        title = product.find_element(By.CSS_SELECTOR, ".dne-itemtile-title").text
    except:
        title = "N/A"

    try:
        price = product.find_element(By.CSS_SELECTOR, ".first").text
    except:
        price = "N/A"

    try:
        original_price = product.find_element(By.CSS_SELECTOR, ".itemtile-price-strikethrough").text
    except:
        original_price = "N/A"

    try:
        shipping = product.find_element(By.CSS_SELECTOR, ".dne-itemtile-delivery").text
    except:
        shipping = "N/A"

    try:
        item_url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        item_url = "N/A"

    data.append([
        timestamp,
        title,
        price,
        original_price,
        shipping,
        item_url
    ])

driver.quit()

file_exists = False

try:
    with open(FILE_NAME, "r"):
        file_exists = True
except:
    file_exists = False

with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow([
            "timestamp",
            "title",
            "price",
            "original_price",
            "shipping",
            "item_url"
        ])

    writer.writerows(data)

print(f"{len(data)} products saved.")