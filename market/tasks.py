import time

from core.models import DribbleProduct, Notification, MarketingPlatforms
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from celery import shared_task


@shared_task
def add(x, y):
    print('STARTING', str(x), str(y))
    time.sleep(10)
    print('DONE', str(x), str(y))
    return x + y

@shared_task
def upload_product_to_dribble(dp, platform):
    options = webdriver.ChromeOptions()
    options.add_argument(' - incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    print('0. STARTED')
    driver = webdriver.Remote(
                command_executor='http://chrome:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options
    )
    try:
        print('DP', dp)
        dp = DribbleProduct.objects.get(id=dp)
        print(dp)
        print('platform', platform)
            # driver = webdriver.Chrome(executable_path=chromedriver_autoinstaller.install(), options=options)
        print('1. DRIVER OPEN')
        driver.get("https://dribbble.com/session/new") # Login URL
        time.sleep(10)
        driver.find_element(By.ID, "login").send_keys('fsiddiqui@students.uit.edu') # add username
        driver.find_element(By.ID, "password").send_keys('faddy3143') # add password
        time.sleep(10)
        driver.find_element(By.CLASS_NAME, "form-sub").click() # click on submit
        print('2. LOGGED IN')

        time.sleep(10)
        driver.get("https://dribbble.com/uploads/new") # upload IMAGE URL
        print('3. UPLOAD URL')
        time.sleep(10)
    
        driver.find_element(By.CLASS_NAME, "drag-drop-input").send_keys(dp.image.path) # UPLOAD IMAGE
        print('4. Image Uploaded')
        time.sleep(30) # sleep to fully upload image

        driver.find_element(By.ID, 'title').send_keys(dp.product.title) # ADD TITLE
        time.sleep(10)
        description_field = driver.find_element(By.CLASS_NAME, 'ProseMirror')
        driver.execute_script("arguments[0].scrollIntoView(true);", description_field)
        description_field.send_keys(
                    f"BUY NOW https://google.com"
        ) # ADD DESCRIPTION
        print('5. Details Added')
        time.sleep(30)

        continue_btn = driver.find_element(By.XPATH, """//button[normalize-space()="Continue"]""")
        time.sleep(10)
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn) # CONTINUE BTN
        continue_btn.click() # CLICK CONTINUE BUTTON
        print('6. Continue Added')
        time.sleep(10)

        driver.find_element(By.TAG_NAME, 'tags').find_element(By.CLASS_NAME, 'tagify__input').send_keys('a,b,c,d,') # ADD TAGS
        print('7. Tags Added')

        publish_btn = driver.find_element(By.XPATH, """//button[normalize-space()="Publish now"]""") # PUBLISH BTM
        publish_btn.click() # CLICK PUBLISH BTN
        print('8. Publish')
        time.sleep(10)

        dribble_id = driver.current_url.split('/')[-1]
        print(f'9. Driver URL, {dribble_id}')
        # driver.find_element(By.CLASS_NAME, "form-sub").click() # click on submit
        # print('2. LOGGED IN')
        # time.sleep(10)
        # driver.get("https://dribbble.com/uploads/new") # upload IMAGE URL
        # print('3. UPLOAD URL')
        # time.sleep(10)
        # driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/label/input").send_keys(dp.image.path) # Upload Image
        # print('4. Image Uploaded')
        # time.sleep(30) # sleep to fully upload image
        # driver.find_element(By.ID, 'title').send_keys(dp.product.title) # ADD TITLE
        # time.sleep(10)
        # driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div/p").send_keys(
        #     f"BUY NOW https://google.com"
        # ) # ADD DESCRIPTION
        # print('5. Details Added')
        # time.sleep(60)
        # continue_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[3]/button[2]")
        # print(continue_btn.text)
        # driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
        # driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[3]/button[2]").click() # CLICK ON CONTINUE
        # print('6. Continue Added')

        # # ADD Tags
        # time.sleep(10)
        # driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/section/div/div/div/div/div[1]/tags/span").send_keys(dp.tags)
        # print('7. Tags Added')
        # # click on publish button
        # driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/section/div/div/div/div/div[8]/div/button[2]").click()
        # print('8. Publish')
        # time.sleep(10)
        # # GET PRODUCT ID
        # dribble_id = driver.current_url.split('/')[-1]
        # print(f'9. Driver URL, {dribble_id}')
        print('WORKING PERFECT.')
        driver.close()
        dp.dribble_id=dribble_id
        dp.status='A'
        dp.save()

        Notification.objects.create(
            user=dp.product.owner,
            content="Your Product listed successfully on dribble.\n we will keep you updated.",
        )

        dp.product.marketed_on.add(MarketingPlatforms.objects.get(title=platform))

    except Exception as e:
        print(e)
        driver.save_screenshot('error.png')
        driver.quit()
    return