from asyncio import wait
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

    #Can be a good thing
    #showDescription = driver.find_element(By.CLASS_NAME, "control-item.control-span-12_12").text

    for idx, card in enumerate(cards, 1):
         eachCard = card.find_element(By.CLASS_NAME,"dadosimovel-col2").text
         eachCard = eachCard.split("\n")

         dias_id = f"dias{idx - 1}"
         horas_id = f"horas{idx - 1}"
         minutos_id = f"minutos{idx - 1}"
         segundos_id = f"segundos{idx - 1}"

         try:
             dias = driver.find_element(By.ID, dias_id).text
             horas = driver.find_element(By.ID, horas_id).text
             minutos = driver.find_element(By.ID, minutos_id).text
             segundos = driver.find_element(By.ID, segundos_id).text
             dias.split(" ")
             horas.split(" ")
             minutos.split(" ")
             segundos.split(" ")
             auction_date = f"{dias[1]} dias, {horas[1]}h {minutos[1]}min {segundos[1]}s"
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
             "id": idx,
             "city": city,
             "price": price,
             "auction_date": auction_date,
             "showDescription": showDescription,
            #"link": link,
            "imageUrl": imageUrl,
            "area": area,
            "banco": "Caixa"
        })

    driver.quit()
    return results