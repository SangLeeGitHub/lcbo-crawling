import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')
# options.add_argument('headless')

driver: WebDriver = webdriver.Chrome('chromedriver', options=options)
wait = WebDriverWait(driver, 5)

driver.get('https://www.lcbo.com/en/products/spirits/tequila')

ve = wait.until(EC.visibility_of(driver.find_element(By.CSS_SELECTOR, '#modal-content-1 > div > div:nth-child(3) > a')))
ve.click()
ve = wait.until(EC.visibility_of(driver.find_element(By.CSS_SELECTOR, '#btn-cookie-allow')))
ve.click()
ve = wait.until(EC.visibility_of(driver.find_element(By.CLASS_NAME, 'my_store_close_button')))
ve.click()

while True:
    try:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        ve = wait.until(EC.visibility_of(driver.find_element(By.CSS_SELECTOR, '#loadMore')))
        ve.click()
        time.sleep(1)
    except selenium.common.exceptions.TimeoutException:
        break

time.sleep(2)

result = driver.find_elements(By.CSS_SELECTOR, '#coveo-result-list2 > div > div')
count = 1

for i in range(1, len(result)):
    v = driver.find_element(By.CSS_SELECTOR, f'#coveo-result-list2 > div > div:nth-child({i})')
    if v.text == '':
        continue
    print(f'{count} ------------------')
    print(v.text)
    print(v.find_element(By.CSS_SELECTOR, "img").get_attribute("src"))
    count += 1

driver.quit()
