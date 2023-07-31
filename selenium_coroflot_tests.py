from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time, os

options = webdriver.FirefoxOptions()
options.add_argument(' - incognito')
# options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Firefox(options=options)
try:
    
    actions = ActionChains(driver)
    driver.get('https://www.coroflot.com/login')
    time.sleep(2)
    driver.find_element(By.ID, 'login_username_email').send_keys('fsiddiqui@students.uit.edu')
    driver.find_element(By.ID, 'login_password').send_keys('faddy3143')
    driver.find_element(By.ID, 'login_password').send_keys(Keys.ENTER)
    time.sleep(5)
    driver.get('https://www.coroflot.com/individual/upload?return_url=/individual')
    time.sleep(2)
    driver.find_element(By.ID, 'upload_image_assets').send_keys(os.getcwd()+"\\03.png")
    time.sleep(10)
    Select(driver.find_element(By.ID, 'select_upload_destination')).select_by_value('0')
    time.sleep(5)
    driver.find_element(By.ID, 'autocomplete_morsel_tag').send_keys('TEST DESCRIPTIOn #AAA')
    time.sleep(2)
    driver.find_element(By.ID, 'autocomplete_morsel_tag').send_keys('S')
    time.sleep(5)
    # driver.find_element(By.XPATH, '//div[normalize-space()="#AAAS"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//span[normalize-space()="Save"]').click()
    time.sleep(10)
    driver.find_element(By.XPATH, '//span[normalize-space()="Publish"]').click()
    time.sleep(2)
    url = [i.get_attribute('href') for i in driver.find_elements(By.TAG_NAME, 'a') if 'https://www.coroflot.com/p/' in i.get_attribute('href')][0]
    print(url)
    print()
except Exception as e:
    print(e)
    driver.save_screenshot('selenium/error.png')
    driver.close()