import os
import tempfile
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Controller.listAll import global_counter
from firebase_admin import credentials, db

def listAllSantander():
    options = Options()
    # options.add_argument('--headless')  
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.santanderimoveis.com.br/?txtsearch=S%C3%A3o+Paulo&cidade=S%C3%A3o+Paulo&view=1")
    time.sleep(3)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "content-cards"))
    )

    results = []

    # Get total number of pages from pagination
    try:
        pagination = driver.find_element(By.CLASS_NAME, "pagination")
        page_links = pagination.find_elements(By.TAG_NAME, "a")
        pages = []
        for link in page_links:
            text = link.text.strip()
            if text.isdigit():
                pages.append(text)
        total_pages = int(pages[-1]) if pages else 1
    except:
        total_pages = 1

    for page in range(1, total_pages + 1):
        if page > 1:
            # Click the page link
            driver.get(f"https://www.santanderimoveis.com.br/?txtsearch=S%C3%A3o+Paulo&cidade=S%C3%A3o+Paulo&view=1&page={page}")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "content-cards"))
            )
            time.sleep(2)

        cards = driver.find_elements(By.CLASS_NAME, "card")
        for card in cards:
            try:
                link = card.get_attribute("href")
            except:
                link = "N/A"
            try:
                # Find the div containing an svg with height="13"
                address_div = card.find_element(By.XPATH, ".//div[.//svg[@height='13']]")
                address = address_div.text.strip()
            except:
                address = "N/A"
            try:
                price = card.find_element(By.CLASS_NAME, "card-valor-ant").text
            except:
                price = "N/A"
            try:
                auction_date = card.find_element(By.CLASS_NAME, "card-data").text
            except:
                auction_date = "N/A"
            try:
                showDescription = card.find_element(By.CLASS_NAME, "card-footer").text
            except:
                showDescription = "N/A"
            try:
                area = card.find_element(By.CLASS_NAME, "card-area").text
            except:
                area = "N/A"
            try:
                imageUrl = card.find_element(By.CLASS_NAME, "card-header").value_of_css_property("background-image")
                imageUrl = imageUrl.replace('url("', '').replace('")', '')
            except:
                imageUrl = "N/A"

            results.append({
                "id": global_counter.global_idx,
                "city": "São Paulo - SP",
                "price": price,
                "auction_date": auction_date,
                "showDescription": showDescription,
                "link": link,
                "imageUrl": imageUrl,
                "area": area,
                "banco": "Santander"
            })
            global_counter.global_idx += 1

    driver.quit()
    ref = db.reference('test_all_banks')
    for entry in results:
        ref.push(entry)
    print("Itau uploaded")

    driver.quit()
    return results

