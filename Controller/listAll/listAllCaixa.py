from asyncio import wait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
from selenium.webdriver.support.ui import Select
import time
from Controller.listAll import global_counter
from firebase_admin import credentials, db

def listAllCaixa():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--enable-unsafe-swiftshader')
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?")

  
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "wrapper"))
    )

    time.sleep(1)

    select = Select(driver.find_element(By.ID, "cmb_estado"))
    select.select_by_visible_text('SP')
    select = Select(driver.find_element(By.ID, "cmb_modalidade"))
    select.select_by_value('33')
    driver.find_element(By.ID, 'btn_next0').click()

    time.sleep(1)

    select = Select(driver.find_element(By.ID, "cmb_tp_imovel"))
    select.select_by_value('4')
    select = Select(driver.find_element(By.ID, "cmb_quartos"))
    select.select_by_value('0')
    select = Select(driver.find_element(By.ID, "cmb_vg_garagem"))
    select.select_by_value('0')
    select = Select(driver.find_element(By.ID, "cmb_area_util"))
    select.select_by_value('0')
    select = Select(driver.find_element(By.ID, "cmb_faixa_vlr"))
    select.select_by_value('0')
    driver.find_element(By.ID, 'btn_next1').click()

    results = []


    # Wait for the first page of results
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "control-group.no-bullets"))
    )

    # Get the number of pages from the pagination
    paginacao = driver.find_element(By.ID, "paginacao")
    page_links = paginacao.find_elements(By.TAG_NAME, "a")
    total_pages = len(page_links)

    for page in range(1, total_pages + 1):
        if page > 1:
            paginacao = driver.find_element(By.ID, "paginacao")
            page_links = paginacao.find_elements(By.TAG_NAME, "a")
            driver.execute_script("arguments[0].click();", page_links[page-1])
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "control-group.no-bullets"))
            )
            time.sleep(1)

        cards = driver.find_elements(By.CLASS_NAME, "control-group.no-bullets")
        for card in cards:
            eachCard = card.find_element(By.CLASS_NAME,"dadosimovel-col2").text
            eachCard = eachCard.split("\n")

           # dias_id = f"dias{cards.index(card)}"
           # horas_id = f"horas{cards.index(card)}"
            #minutos_id = f"minutos{cards.index(card)}"
           # segundos_id = f"segundos{cards.index(card)}"

            try:
                #dias = driver.find_element(By.ID, dias_id).text
               # horas = driver.find_element(By.ID, horas_id).text
                #minutos = driver.find_element(By.ID, minutos_id).text
               #segundos = driver.find_element(By.ID, segundos_id).text
                auction_date = "Não informado"
            except:
                auction_date = "N/A"
            
            try:
                city = eachCard[0]
            except:
                city = "N/A"
            
            try:
                price = eachCard[1]
            except:
                price = "N/A"
            
            try:
                showDescription = eachCard[6]
            except:
                showDescription = "N/A"
            try:
                area = "Não informado"
            except:
                area = "Não informado"
            try:
                imageUrl = card.find_element(By.CLASS_NAME,"fotoimovel").get_attribute("src")
                imageUrl = "https://venda-imoveis.caixa.gov.br" + imageUrl
            except:
                imageUrl = "N/A"
            
            results.append({
                "id": global_counter.global_idx,
                "link": "Não informado",
                "city": city,
                "price": price,
                "auction_date": auction_date,
                "showDescription": showDescription,
                "imageUrl": imageUrl,
                "area": area,
                "banco": "Caixa"
            })

            global_counter.global_idx += 1

    driver.quit()
    ref = db.reference('test_all_banks')
    for entry in results:
        ref.push(entry)
    print("Itau uploaded")

    driver.quit()
    return results

