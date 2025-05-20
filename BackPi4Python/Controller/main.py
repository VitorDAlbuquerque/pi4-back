from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import time

def scrapper():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.itau.com.br/imoveis-itau?estado=S%C3%83O+PAULO")
    time.sleep(20)  # Wait for JS to render

    # Debug: print shadow DOM HTML
    print(driver.execute_script("return document.querySelector('.itau-leiloes-list')?.shadowRoot?.innerHTML"))

    # Use JS to access shadow DOM and extract info from each card
    cards = driver.execute_script("""
        const appRoot = document.querySelector("app-leiloes-list");
        if (!appRoot) return [];
        const shadow = appRoot.shadowRoot;
        if (!shadow) return [];
        let container = shadow.querySelector(".itau-leiloes-pagination-cards");
        if (!container) return [];
        container = container.querySelector(".ng-star-inserted");
        container = container.querySelector(".itau-leiloes-card")
        container = container.querySelector(".itau-leiloes-card-info")
        container = container.querySelector(".itau-leiloes-card-info-upper")
        return Array.from(container.querySelectorAll(".itau-leiloes-card-info-upper")).map(card => {
            const getText = (selector) => {
                const el = card.querySelector(selector);
                return el ? el.textContent.trim() : null;
            };
            return {
                name: getText('.itau-leiloes-card-info-address'),
                address: getText('.itau-leiloes-card-info-street_address'),
                price: getText('.itau-leiloes-card-info-type')
            };
        });
    """)

    driver.quit()

    # Print results in a readable way
    for idx, card in enumerate(cards, 1):
        print(f"Imóvel {idx}:")
        print(f"  Nome: {card['name']}")
        print(f"  Endereço: {card['address']}")
        print(f"  Valor: {card['price']}")
        print("-" * 30)


    print("Quantity a:", len(cards))
    return cards
