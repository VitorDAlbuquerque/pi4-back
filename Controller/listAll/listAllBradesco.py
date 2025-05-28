import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numbers

import tempfile
import time

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

 
    last_count = 0
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(1.1)
        cards = driver.find_elements(By.CLASS_NAME, "auction-container")
        if len(cards) == last_count:
            break
        last_count = len(cards)

    results = []
    
   
    for idx, card in enumerate(cards, 1):
        idBanco = idx
        description = card.find_element(By.CLASS_NAME, "description").text.split("|")
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
            area = description[1].find("m²")
            area = description[1][area - 6: area+2].strip()
        except:
            area = "N/A"
        try:
            imageUrl = card.find_element(By.CLASS_NAME, "lazy-thumbnail").get_attribute("src")
        except:
            imageUrl = "N/A"
        results.append({
            "id": idBanco,
            "city": city,
            "price": price,
            "auction_date": auction_date,
            "showDescription": showDescription,
            "link": link,
            "imageUrl": imageUrl,
            "area": area,
            "banco": "Bradesco"
        })

    
    driver.quit()

    for idx, item in enumerate(results, 1):
        print(f"Imóvel {idBanco}:")
        print(f"  Cidade: {item['city']}")
        print(f"  Valor: {item['price']}")
        print(f"  {item['auction_date']}")
        print(f"  Description: {item['showDescription']}")
        print(f"  Link: {item['link']}")
        print(f"URL Image: {imageUrl}")
        print(f"area:  {area}")
        print("-" * 30)

    print("Quantidade:", len(results))
    return results