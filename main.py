import time
import datetime
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
# options.add_argument('headless')

driver: WebDriver = webdriver.Chrome('chromedriver', options=options)
wait = WebDriverWait(driver, 5)

urls = {'tequila': 'https://www.lcbo.com/en/products/spirits/tequila',
        'rum': 'https://www.lcbo.com/en/products/spirits/rum',
        'soju': 'https://www.lcbo.com/en/products/spirits/soju',
        }

first_word = ['Online Exclusive', 'On Sale', 'New Arrival', 'AEROPLAN', 'VINTAGES', 'Clearance', 'Best Seller']
driver.get('https://www.lcbo.com')

ve = wait.until(EC.visibility_of(driver.find_element(By.CSS_SELECTOR, '#modal-content-1 > div > div:nth-child(3) > a')))
ve.click()
ve = wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, '#btn-cookie-allow')))
ve.click()
ve = wait.until(EC.element_to_be_clickable(driver.find_element(By.CLASS_NAME, 'my_store_close_button')))
ve.click()

for key, value in urls.items():
    driver.get(value)
    while True:
        try:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            ve = wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, '#loadMore')))
            ve.click()
            time.sleep(1)
        except TimeoutException:
            break

    time.sleep(2)

    result = driver.find_elements(By.CSS_SELECTOR, '#coveo-result-list2 > div > div')
    count = 1

    filename = key + ' ' + str(datetime.datetime.now()) + '.csv'
    f = open(filename, "w")

    for i in range(1, len(result)):
        line = []
        v = driver.find_element(By.CSS_SELECTOR, f'#coveo-result-list2 > div > div:nth-child({i})')
        if v.text == '':
            continue
        text = v.text.splitlines()
        if text[0] in first_word:
            text.pop(0)
        if text[1].__contains__('$'):
            text.insert(1, ' ')
        if text[2].__contains__('('):
            text.pop(2)
        if text[2].__contains__('$') and text[3].__contains__('$'):
            text.pop(2)
        f.write(text[0] + ',' + text[1] + ',' + text[2] + ','
                + v.find_element(By.CSS_SELECTOR, "img").get_attribute("src") + '\n')
        count += 1
        print('Wrote item number ' + str(count))

    print("Saved " + filename + " - " + str(count) + " items")
    f.close()

driver.quit()
