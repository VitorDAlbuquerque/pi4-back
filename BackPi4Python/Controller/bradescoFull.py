from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
import time
import requests
from bs4 import BeautifulSoup


def fetch_detail(link):
    try:
        resp = requests.get(link, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Example: get the auction button text
        auction_btn = soup.find("button", string=lambda s: s and "Participar do leilão" in s)
        auction_button = auction_btn.text.strip() if auction_btn else "N/A"
        return auction_button
    except Exception as e:
        return "N/A"

def bradescoFull():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://vitrinebradesco.com.br/auctions?type=realstate&ufs=SP")

    # Wait for the first card to load (max 10s)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "auction-container"))
    )

    # Scroll until all cards are loaded
    last_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.7)  # Faster scroll wait
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
        try:
            link = card.get_attribute("href")
            if link and link.startswith("/"):
                link = "https://vitrinebradesco.com.br" + link
        except:
            link = "N/A"

        results.append({
            "city": city,
            "price": price,
            "auction_date": auction_date,
            "showDescription": showDescription,
            "link": link
        })

    driver.quit()

    # Print results
    for idx, item in enumerate(results, 1):
        print(f"Imóvel {idx}:")
        print(f"  city: {item['city']}")
        print(f"  Valor: {item['price']}")
        print(f"  Data do Leilão: {item['auction_date']}")
        print(f"  Description: {item['showDescription']}")
        print(f"  Link: {item['link']}")
        print("-" * 30)

    print("Quantidade:", len(results))
    return results