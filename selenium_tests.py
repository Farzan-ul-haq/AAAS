from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time

options = webdriver.ChromeOptions()
options.add_argument(' - incognito')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(executable_path=chromedriver_autoinstaller.install(), options=options)
print('1. DRIVER OPEN')
driver.get("https://dribbble.com/session/new") # Login URL
driver.save_screenshot('1.png')
time.sleep(10)
driver.find_element(By.ID, "login").send_keys('fsiddiqui@students.uit.edu') # add username
driver.find_element(By.ID, "password").send_keys('faddy3143') # add password
time.sleep(10)
driver.save_screenshot('2.png')
driver.find_element(By.CLASS_NAME, "form-sub").click() # click on submit
print('2. LOGGED IN')
time.sleep(10)
driver.quit()