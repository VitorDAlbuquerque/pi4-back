from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

try:
    url = "https://vitrinebradesco.com.br/auctions/casa-santo-andresp-al-sebastiao-do-amaral-366-bairro-vila-tibirica-9_1"
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    participate_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "participate")))
    button = participate_div.find_element(By.TAG_NAME, "button")
    button.click()

    wait.until(lambda d: len(d.window_handles) > 1)
    windows = driver.window_handles
    if len(windows) > 1:
        driver.switch_to.window(windows[1])
        new_url = driver.current_url
        print("New tab URL:", new_url)
    else:
        print("No new tab detected.")

finally:
    driver.quit()