from asyncio import wait
def listAllItau():
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    import tempfile
    import time
    from firebase_admin import credentials, db
    import re
    from Controller.listAll import global_counter

    def expand_shadow_element(driver, element):
        return driver.execute_script('return arguments[0].shadowRoot', element)

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    driver = uc.Chrome(options=options)
    driver.get("https://www.itau.com.br/imoveis-itau?leilao=true&estado=S%C3%83O+PAULO")
    time.sleep(8)  # Wait for JS to load

    # Find the app-leiloes-list shadow root
    for _ in range(40):
        try:
            app_leiloes_list = driver.find_element(By.CSS_SELECTOR, "app-leiloes-list")
            break
        except:
            time.sleep(1)
    else:
        print("app-leiloes-list not found!")
        driver.quit()
        return []

    shadow_root = expand_shadow_element(driver, app_leiloes_list)

    # Now get all itau-leiloes-card elements inside the shadow root
    max_wait = 30
    waited = 0
    cards = []
    while waited < max_wait:
        cards = shadow_root.find_elements(By.CSS_SELECTOR, "itau-leiloes-card")
        if len(cards) > 0:
            break
        time.sleep(1)
        waited += 1

    if not cards:
        print("No cards found after waiting.")
        driver.quit()
        return []

    # Load all cards by clicking "carregar mais" until the button is disabled or not found
    while True:
        try:
            carregar_btn = shadow_root.find_element(
                By.CSS_SELECTOR,
                'button[data-testid="itau-leiloes-button-carregar-mais"]:not([disabled])'
            )
            if carregar_btn.is_displayed():
                # Scroll the button into view before clicking
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", carregar_btn)
                time.sleep(0.5)  # Give time for scroll
                carregar_btn.click()
                time.sleep(2)  # Wait for new cards to load
            else:
                break
        except Exception:
            break

    # Re-fetch cards after loading more
    cards = shadow_root.find_elements(By.CSS_SELECTOR, "itau-leiloes-card")

    results = []
    for card in cards:
        # Title (city + state)
        try:
            title = card.find_element(By.CSS_SELECTOR, 'h4[data-testid$="info-address"]').text
        except Exception as e:
            print("Title not found:", e)
            title = "N/A"
        # Address
        try:
            address = card.find_element(By.CSS_SELECTOR, 'p[data-testid$="info-street_address"]').text
        except Exception as e:
            print("Address not found:", e)
            address = "N/A"
        # Area (only the number and m², e.g., "120m²")
        try:
            area_text = card.find_element(By.CSS_SELECTOR, 'div[data-testid$="info-type"]').text
            match = re.search(r'\d+\s?m²', area_text.lower())
            area = match.group(0) if match else "N/A"
        except Exception as e:
            print("Area not found:", e)
            area = "N/A"
        # Price (only "R$" and the number)
        try:
            price_text = card.find_element(By.CSS_SELECTOR, 'div[data-testid$="info-current_price"]').text
            match = re.search(r'R\$\s?[\d\.,]+', price_text)
            price = match.group(0) if match else "N/A"
        except Exception as e:
            print("Price not found:", e)
            price = "N/A"
        # Image URL
        try:
            img = card.find_element(By.CSS_SELECTOR, ".itau-leiloes-card-header img, .itau-leiloes-card-carrousel img")
            imageUrl = img.get_attribute("src")
        except Exception as e:
            print("Image not found:", e)
            imageUrl = "N/A"
        # Auction date
        try:
            auction_date = card.find_element(By.CSS_SELECTOR, 'span[data-testid^="itau-leiloes-tag-"][class*="tag-label"]').text
        except Exception as e:
            print("Auction date not found:", e)
            auction_date = "N/A"

        # Link (extract only the number from "código do imovel: 920176")
        try:
            code_spans = card.find_elements(By.CSS_SELECTOR, 'span[data-testid^="itau-leiloes-tag-"]')
            link = "N/A"
            for span in code_spans:
                text = span.text.strip()
                if text.lower().startswith("código do imovel"):
                    match = re.search(r'\d+', text)
                    if match:
                        link = match.group(0)
                        link = f"https://www.itau.com.br/imoveis-itau/detalhes?id={link}"
                    break
        except Exception as e:
            print("Link (code) not found:", e)
            link = "N/A"

        results.append({
            "id": global_counter.global_idx,
            "City": title,
            "showDescription": address,
            "area": area,
            "price": price,
            "imageUrl": imageUrl,
            "auction_date": auction_date,
            "link": link,
            "banco": "Itau"
        })
        global_counter.global_idx += 1

    driver.quit()
    ref = db.reference('test_all_banks')
    for entry in results:
        ref.push(entry)
    print("Itau uploaded")

    return results
