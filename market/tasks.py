import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from celery import shared_task

from core.models import DribbleProduct, Notification, MarketingPlatforms, \
    CoroloftProduct, PinterestProduct


options = webdriver.ChromeOptions()
options.add_argument(' - incognito')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")


@shared_task
def add(x, y):
    print('STARTING', str(x), str(y))
    time.sleep(10)
    print('DONE', str(x), str(y))
    return x + y

@shared_task
def upload_product_to_dribble(dp, platform):
    driver = webdriver.Remote(
                command_executor='http://chrome:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options
    )
    print('0. STARTED')
    try:
        dp = DribbleProduct.objects.get(id=dp)
        print(dp)
        print(platform)
            # driver = webdriver.Chrome(executable_path=chromedriver_autoinstaller.install(), options=options)
        print('1. DRIVER OPEN')
        driver.get("https://dribbble.com/session/new") # Login URL
        time.sleep(10)
        driver.find_element(By.ID, "login").send_keys('farzanulhaq12@gmail.com') # add username
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
        description_field.send_keys(dp.description) # ADD DESCRIPTION
        description_field.click() # CLICK DESCRIPTION TEXT TO SEE THE RIGHT ALIGN BUTTON
        time.sleep(5)
        driver.find_element(By.XPATH, '//button[@data-test="button-item-center"]').click() # CENTER ALIGN BUTTON CLICK
        print(dp.description)
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


@shared_task
def upload_product_to_pinterest(pp, platform):
    driver = webdriver.Remote(
                command_executor='http://chrome:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options
    )
    print('0. STARTED')
    print('PINTEREST WORKING...')
    try:
        pp = PinterestProduct.objects.get(id=pp)
        actions = ActionChains(driver)
        driver.get("https://www.pinterest.com/")
        print('1. GO TO PINTEREST URL')
        time.sleep(5)
        driver.find_element(By.XPATH, """//div[normalize-space()="Log in"]""").click() # CLICK LOGIN BUTTON
        print('2. CLICK LOGIN BUTTON')
        time.sleep(10)
        driver.find_element(By.ID, 'email').send_keys('fsiddiqui@students.uit.edu') # ADD EMAIl
        print('3. ADD EMAIL')
        time.sleep(2)
        driver.find_element(By.ID, 'password').send_keys('faddy3143') # ADD PASSWORD
        print('4. ADD PASSWORD')
        time.sleep(2)
        driver.find_element(By.XPATH, """//div[@data-test-id='registerFormSubmitButton']""").click() # CLICK LOGIN BUTTOn
        print('5. CLICK LOGIN SUBMIT BTN')
        time.sleep(10)
        driver.get('https://www.pinterest.com/pin-builder/') # GO TO CREATE PIN URL
        print('6. CREATE PIN URL')
        time.sleep(5)
        title_weburl_textarea = driver.find_element(
            By.XPATH, 
            "//div[@data-tutorial-id='pin-builder-title-and-description']"
        ).find_elements(By.XPATH, '//textarea') # COLLECT TEXTAREA
        for tag in title_weburl_textarea:
            try:
                if "title" in tag.get_attribute('placeholder'):
                    tag.send_keys(pp.title) # ADD TITLE
                    print('7. ADD TITLE')
                elif "link" in tag.get_attribute('link'):
                    tag.send_keys(pp.redirect_url) # ADD DESTINATION CLICK
                    print('8. ADD DESTINATION LINK')
                time.sleep(2)
            except Exception as e:
                pass
        time.sleep(2)
        description_span = driver.find_element(
            By.XPATH, 
            "//div[@data-tutorial-id='pin-builder-title-and-description']"
        ).find_elements(By.XPATH, '//span') # COLLECT SPAN
        for span in description_span:
            try:
                span.send_keys(pp.description) # ADD DESCRIPTION
                print('9. ADD DESCRIPTION')
                time.sleep(2)
            except Exception as e:
                pass
        driver.find_element(By.XPATH, "//input[@aria-label='File upload']").send_keys(pp.image.path) # UPLOAD IMAGE
        time.sleep(20)
        print('10. UPLOAD IMAGE')
        driver.find_element(By.XPATH, "//button[@data-test-id='board-dropdown-save-button']").click() # CLICK PUBLISH BUTTON
        time.sleep(50)
        print('11. CREATE PUBLISH BUTTON')
        driver.get('https://www.pinterest.com/AAAS01/products/') # GO TO PRODUCTS URL
        time.sleep(15)
        print('12. GO TO MY PRODUCTS URL')
        pinterest_id = [
            i.get_attribute('href') 
            for i in driver.find_elements(By.XPATH, '//a') 
            if 'https://www.pinterest.com/pin/' in i.get_attribute('href')
        ][0].replace('https://www.pinterest.com/pin/', '')
        driver.close()
        pp.pinterest_id = pinterest_id
        pp.status = "A"
        pp.save()

        Notification.objects.create(
            user=pp.product.owner,
            content="Your Product listed successfully on Pinterest.\n we will keep you updated.",
        )
        pp.product.marketed_on.add(MarketingPlatforms.objects.get(title=platform))
        print('13. PUBLISHED ON PINTEREST')
    except Exception as e:
        print("ERROR: ",e)
        driver.save_screenshot('error.png')
        driver.quit()
    return

@shared_task
def upload_product_to_coroflot(cp, platform):
    driver = webdriver.Remote(
                command_executor='http://chrome:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options
    )
    print('0. STARTED')
    print('COROFLOT WORKING...')
    try:
        cp = CoroloftProduct.objects.get(id=cp)
        actions = ActionChains(driver)
        driver.get('https://www.coroflot.com/login') # CLICK LOGIN
        time.sleep(2)
        print('1. LOGIN URL')
        driver.find_element(By.ID, 'login_username_email').send_keys('fsiddiqui@students.uit.edu') # ADD EMAIL
        print('2. EMAIL ADDED')
        time.sleep(2)
        driver.find_element(By.ID, 'login_password').send_keys('faddy3143') # ADD PASSWORD
        print('3. PASSWORD ADDED')
        time.sleep(2)
        driver.find_element(By.ID, 'login_password').send_keys(Keys.ENTER) # PRESS ENTER
        print('4. LOGIN SUBMIT')
        time.sleep(5)
        driver.get('https://www.coroflot.com/individual/upload?return_url=/individual') # GO TO CREATE URL
        print('5. CREATE POST URL')
        time.sleep(2)
        driver.find_element(By.ID, 'upload_image_assets').send_keys(cp.image.path) # UPLOAD IMAGE
        print('6. IMAGE UPLOADED')
        time.sleep(10)
        Select(driver.find_element(By.ID, 'select_upload_destination')).select_by_value('0') # SELECT STANDALONE POST
        print('7. SELECT STANDALONE POST')
        time.sleep(5)
        driver.find_element(By.ID, 'autocomplete_morsel_tag').send_keys(cp.description) # ADD DESCRIPTION
        time.sleep(2)
        driver.find_element(By.ID, 'autocomplete_morsel_tag').send_keys(" #AAA") # ADD DESCRIPTION
        driver.find_element(By.ID, 'autocomplete_morsel_tag').send_keys("S") # ADD DESCRIPTION
        print('8. DESCRIPTION ADDED')
        time.sleep(10)
        try:
            driver.find_element(By.XPATH, '//div[normalize-space()="#AAAS"]').click()
            print('9. SELECT HASHTAG')
        except Exception as e:
            print(e)
        time.sleep(3)
        driver.find_element(By.XPATH, '//span[normalize-space()="Save"]').click()
        print('10. SAVE DESCRIPTION')
        time.sleep(2)
        driver.find_element(By.XPATH, '//span[normalize-space()="Publish"]').click()
        print('11. PUBLISHED')
        time.sleep(2)
        coroflot_id = [
            i.get_attribute('href') 
            for i in driver.find_elements(By.TAG_NAME, 'a') 
            if 'https://www.coroflot.com/p/' in i.get_attribute('href')
        ][0].replace('https://www.coroflot.com/p/', '')
        driver.close()
        print(f'12. {coroflot_id}')
        cp.coroflot_id = coroflot_id
        cp.status = "A"
        cp.save()

        Notification.objects.create(
            user=cp.product.owner,
            content="Your Product listed successfully on Coroflot.\n we will keep you updated.",
        )
        cp.product.marketed_on.add(MarketingPlatforms.objects.get(title=platform))

    except Exception as e:
        print("ERROR: ",e)
        driver.save_screenshot('error.png')
        driver.quit()
    return
        
