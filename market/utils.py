import time

from core.models import DribbleProduct, Notification
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller


def upload_product_to_dribble(product, title, description, tags, image, platform):
    options = webdriver.ChromeOptions()
    options.add_argument(' - incognito')
    # options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options)

    driver.get("https://dribbble.com/session/new") # Login URL
    time.sleep(10)
    driver.find_element(By.ID, "login").send_keys('fsiddiqui@students.uit.edu') # add username
    driver.find_element(By.ID, "password").send_keys('faddy3143') # add password
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "form-sub").click() # click on submit

    driver.get("https://dribbble.com/uploads/new") # upload IMAGE URL
    time.sleep(10)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/label/input").send_keys(image.path) # Upload Image
    time.sleep(30) # sleep to fully upload image
    driver.find_element(By.ID, 'title').send_keys(product.title) # ADD TITLE
    time.sleep(30)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div/p").send_keys(
        f"BUY NOW https://google.com"
    ) # ADD DESCRIPTION
    time.sleep(60)
    print(driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[3]/button[2]").text)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[3]/button[2]").click() # CLICK ON CONTINUE

    # ADD Tags
    time.sleep(10)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/section/div/div/div/div/div[1]/tags/span").send_keys(tags)

    # click on publish button
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/section/div/div/div/div/div[8]/div/button[2]").click()

    time.sleep(10)
    # GET PRODUCT ID
    dribble_id = driver.current_url.split('/')[-1]

    driver.quit()

    DribbleProduct.objects.create(
        product=product,
        title=title,
        views=0,
        description=description,
        dribble_id=dribble_id,
        image=image
    )
    Notification.objects.create(
        user=product.owner,
        content="Your Product listed successfully on dribble.\n we will keep you updated.",
    )
    product.marketed_on.add(MarketingPlatforms.objects.get(title=platform))