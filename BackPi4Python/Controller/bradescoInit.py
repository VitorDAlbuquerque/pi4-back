from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import tempfile
import time

def bradescoInit():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://vitrinebradesco.com.br/auctions?type=realstate&ufs=SP")
    time.sleep(5)  


    last_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        cards = driver.find_elements(By.CLASS_NAME, "auction-container")
        if len(cards) == last_count:
            break 
        last_count = len(cards)

    results = []

    for idx, card in enumerate(cards, 1):
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



        results.append({
            "city": city,
            "price": price,
            "auction_date": auction_date,
            "showDescription": showDescription
        })

        print(f"Imóvel {idx}:")
        print(f"  city: {city}")
        print(f"  Valor: {price}")
        print(f"  Data do Leilão: {auction_date}")
        print(f"  Description: {showDescription}")
        print("-" * 30)

    print("Quantidade:", len(results))
    driver.quit()
    return results
