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
    print('1. DRIVER OPEN')
    driver.get("https://dribbble.com/session/new") # Login URL
    driver.save_screenshot('selenium/1.png')
    time.sleep(10)
    driver.find_element(By.ID, "login").send_keys('farzanulhaq12@gmail.com') # add username
    driver.find_element(By.ID, "password").send_keys('faddy3143') # add password
    time.sleep(10)
    driver.save_screenshot('selenium/2.png')
    driver.find_element(By.CLASS_NAME, "form-sub").click() # click on submit
    print('2. LOGGED IN')
    time.sleep(10)
    driver.get("https://dribbble.com/uploads/new") # upload IMAGE URL
    driver.save_screenshot('selenium/3.png')
    print('3. UPLOAD URL')
    time.sleep(10)
    driver.find_element(By.CLASS_NAME, "drag-drop-input").send_keys(os.getcwd()+"\\01.png")
    driver.save_screenshot('selenium/4.png')
    print('4. Image Uploaded')
    time.sleep(30) # sleep to fully upload image
    driver.find_element(By.ID, 'title').send_keys("01") # ADD TITLE
    time.sleep(10)

    description_field = driver.find_element(By.CLASS_NAME, 'ProseMirror')
    driver.execute_script("arguments[0].scrollIntoView(true);", description_field)
    description_field.send_keys(
                """FontLab 2022 is a reliable and powerful Font developing and editing application which allows you to design and edit your favorite fonts in a professional graphical environment. It is a comprehensive font editor which comes loaded with a professional and full-featured toolset for creating and customizing fonts. It is the ultimate integrated font editor that helps you create fonts from start to finish, from a simple design to a really ultra bold complex project. It supports all popular font formats, including Type 1, TrueType, PostScript, Web fonts, Multiple Master, OpenType, and more.The program offers an easy-to-use interface that provides easy access to all tools. You can also download Summitsoft Creative Fonts Collection 2021 Free Download. Simplify your daily operations with our user-friendly software - Buy now! http://localhost:8000/product/137-fontslab-2022/"""
    )
    description_field.click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//button[@data-test="button-item-center"]').click()
    driver.save_screenshot('selenium/5.png')
    print('5. Details Added')
    time.sleep(30)
    continue_btn = driver.find_element(By.XPATH, """//button[normalize-space()="Continue"]""")
    time.sleep(10)
    driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
    continue_btn.click()
    print('6. Continue Added')
    driver.save_screenshot('selenium/6.png')
    time.sleep(10)
    driver.find_element(By.TAG_NAME, 'tags').find_element(By.CLASS_NAME, 'tagify__input').send_keys('a,b,c,d,')
    print('7. Tags Added')
    driver.save_screenshot('selenium/7.png')
    publish_btn = driver.find_element(By.XPATH, """//button[normalize-space()="Publish now"]""")
    publish_btn.click()
    print('8. Publish')
    driver.save_screenshot('selenium/8.png')
    time.sleep(10)
    # GET PRODUCT ID
    dribble_id = driver.current_url.split('/')[-1]
    print(f'9. Driver URL, {dribble_id}')
    driver.save_screenshot('selenium/9.png')
    driver.close()
except Exception as e:
    print(e)
    driver.save_screenshot('selenium/error.png')
    driver.close()