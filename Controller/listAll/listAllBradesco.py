import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
import time
from Controller.listAll import global_counter
from firebase_admin import credentials, db

def listAllBradesco():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://vitrinebradesco.com.br/auctions?type=realstate&ufs=SP")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "auction-container"))
    )

    # Get total number of pages from pagination
    try:
        pagination = driver.find_element(By.CLASS_NAME, "pagination")
        page_links = pagination.find_elements(By.TAG_NAME, "a")
        total_pages = int(page_links[-2].text)  # Usually the last page number is the second to last <a>
    except Exception:
        total_pages = 1

    results = []

    for page in range(1, total_pages + 1):
        if page > 1:
            # Click the page number link
            pagination = driver.find_element(By.CLASS_NAME, "pagination")
            page_links = pagination.find_elements(By.TAG_NAME, "a")
            for link in page_links:
                if link.text == str(page):
                    driver.execute_script("arguments[0].click();", link)
                    time.sleep(2)
                    break

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "auction-container"))
        )
        cards = driver.find_elements(By.CLASS_NAME, "auction-container")

        for card in cards:
            try:
                description = card.find_element(By.CLASS_NAME, "description").text.split("|")
            except:
                description = ["N/A", "N/A"]
            try:
                city = card.find_element(By.CLASS_NAME, "location").text.strip()
            except:
                city = "N/A"
            try:
                price = card.find_element(By.CLASS_NAME, "price").text.split("\n")[0].strip()
            except:
                price = "N/A"
            try:
                auction_date = description[0]
            except:
                auction_date = "N/A"
            try:
                showDescription = description[1]
            except:
                showDescription = "N/A"
            try:
                link = card.get_attribute("href")
                if link and link.startswith("/"):
                    link = "https://vitrinebradesco.com.br" + link
            except:
                link = "N/A"
            try:
                area_idx = description[1].find("m²")
                area = description[1][area_idx - 6: area_idx+2].strip() if area_idx > 6 else "N/A"
            except:
                area = "N/A"
            try:
                imageUrl = card.find_element(By.CLASS_NAME, "lazy-thumbnail").get_attribute("src")
            except:
                imageUrl = "N/A"

            results.append({
                "id": global_counter.global_idx,
                "city": city,
                "price": price,
                "auction_date": auction_date,
                "showDescription": showDescription,
                "link": link,
                "imageUrl": imageUrl,
                "area": area,
                "banco": "Bradesco"
            })

            print(f"Imóvel {global_counter.global_idx}:")
            print(f"  Cidade: {city}")
            print(f"  Valor: {price}")
            print(f"  {auction_date}")
            print(f"  Description: {showDescription}")
            print(f"  Link: {link}")
            print(f"URL Image: {imageUrl}")
            print(f"area:  {area}")
            print("-" * 30)

            global_counter.global_idx += 1

    driver.quit()
    ref = db.reference('test_all_banks')
    for entry in results:
        ref.push(entry)
    print("Itau uploaded")

    print("Quantidade:", len(results))
    return results