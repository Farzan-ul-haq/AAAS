from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time, os

options = webdriver.ChromeOptions()
options.add_argument(' - incognito')
# options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(executable_path=chromedriver_autoinstaller.install(), options=options)
try:
    driver.get("https://www.pinterest.com/")
    time.sleep(5)
    driver.find_element(By.XPATH, """//div[normalize-space()="Log in"]""").click() # CLICK LOGIN BUTTON
    time.sleep(2)
    driver.find_element(By.ID, 'email').send_keys('fsiddiqui@students.uit.edu') # ADD EMAIl
    time.sleep(2)
    driver.find_element(By.ID, 'password').send_keys('faddy3143') # ADD PASSWORD
    time.sleep(2)
    driver.find_element(By.XPATH, """//div[@data-test-id='registerFormSubmitButton']""").click() # CLICK LOGIN BUTTOn
    time.sleep(2)
    driver.get('https://www.pinterest.com/pin-builder/') # GO TO CREATE PIN URL
    time.sleep(5)
    title_weburl_textarea = driver.find_element(By.XPATH, "//div[@data-tutorial-id='pin-builder-title-and-description']").find_elements(By.XPATH, '//textarea') # COLLECT TEXTAREA
    print(len(title_weburl_textarea))
    for tag in title_weburl_textarea:
        try:
            if "title" in tag.get_attribute('placeholder'):
                tag.send_keys('TEST TITLE') # ADD TITLE
            elif "link" in tag.get_attribute('link'):
                tag.send_keys(('https://google.com')) # ADD DESTINATION CLICK
            time.sleep(2)
        except Exception as e:
            print(e)
    time.sleep(2)
    description_span = driver.find_element(By.XPATH, "//div[@data-tutorial-id='pin-builder-title-and-description']").find_elements(By.XPATH, '//span') # COLLECT SPAN
    for span in description_span:
        try:
            span.send_keys('TEST DESCRIPTION') # ADD DESCRIPTION
            time.sleep(2)
        except Exception as e:
            print(e) # IGNORE OTHER SPAN TAGS
            print(span.text)
    driver.find_element(By.XPATH, "//input[@aria-label='File upload']").send_keys(os.getcwd()+"\\03.png") # UPLOAD IMAGE
    driver.find_element(By.XPATH, "//button[@data-test-id='board-dropdown-save-button']").click() # CLICK PUBLISH BUTTON
    time.sleep(50)
    driver.get('https://www.pinterest.com/AAAS01/products/') # GO TO PRODUCTS URL
    time.sleep(2)
    a_tags = [i.get_attribute('href') for i in driver.find_elements(By.XPATH, '//a') if '/pin/' in i.get_attribute('href')]
    print(a_tags[0])
    print()
except Exception as e:
    print(e)
    driver.save_screenshot('selenium/error.png')
    driver.close()