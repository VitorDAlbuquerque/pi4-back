from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
from selenium.webdriver.support.ui import Select
import time

def listAllCaixa():
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?")

  
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "wrapper"))
    )


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

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "control-group.no-bullets"))
    )


    last_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.7) 
        cards = driver.find_elements(By.CLASS_NAME, "control-group.no-bullets")
        if len(cards) == last_count:
            break
        last_count = len(cards)
    

    results = []

    for idx, card in enumerate(cards, 1):
        title =  city = card.find_element(By.TAG_NAME, "a").text.split("-")
        try:
            city = title[0]
        except:
            city = "N/A"
        
        try:
            valor = driver.find_elements(By.TAG_NAME, "font[style='font-size:0.80em;']")
        except:
            valor = "n/a"
        # try:
        #     price = card.find_element(By.CLASS_NAME, "price").text.split("\n")[0].strip()
        # except:
        #     price = "N/A"
        # try:
        #     auction_date = description[0]
        # except:
        #     auction_date = "N/A"
        # try:
        #     showDescription = description[1]
        # except:
        #     showDescription = "N/A"
        # try:
        #     link = card.get_attribute("href")
        #     if link and link.startswith("/"):
        #         link = "https://vitrinebradesco.com.br" + link
        # except:
        #     link = "N/A"
        # try:
        #     imageUrl = card.find_element(By.CLASS_NAME, "lazy-thumbnail").get_attribute("src")
        # except:
        #     imageUrl = "N/A"
        # results.append({
        #     "city": city,
        #     "price": price,
        #     "auction_date": auction_date,
        #     "showDescription": showDescription,
        #     "link": link,
        #     "imageUrl": imageUrl,
        #     "banco": "Bradesco"
        # })

        print(city)
        print(valor)

    driver.quit()
listAllCaixa()