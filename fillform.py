import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


# ----------------- Main Function -----------------
def fillform(name, nmc_no, education):
    driver = None
    try:
        driver = setupDriver()
        driver.get("https://www.nmc.org.np/search-registered-doctor/")

        # ---- Fill the form ----
        fill_input(driver, By.ID, "name", name)
        fill_input(driver, By.ID, "symbol", nmc_no)
        fill_input(driver, By.NAME, "degreed", education)

        # ---- Click Search button ----
        waitToLoad(driver, By.XPATH, "//button[span[text()='Search']]")
        driver.find_element(By.XPATH, "//button[span[text()='Search']]").click()

        haltStep()

        # ---- Check if result exists ----
        try:
            waitToLoad(
                driver,
                By.CSS_SELECTOR,
                ".mt-5.col-md-6.col-lg-6.col-sm-12",
                timeout=5
            )
            result = "yes"
        except:
            result = "no"

        return result

    except Exception as e:
        print("Selenium Error:", e)
        return "no"

    finally:
        if driver:
            driver.quit()


# ----------------- Setup Brave Driver -----------------
def setupDriver():
    options = uc.ChromeOptions()

    # 🔥 IMPORTANT: Set Brave browser path
    options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # You can enable headless later if needed
    # options.add_argument("--headless=new")

    driver = uc.Chrome(options=options, use_subprocess=True)

    driver.implicitly_wait(10)
    return driver


# ----------------- Helper Functions -----------------
def fill_input(driver, by_type, identifier, value):
    waitToLoad(driver, by_type, identifier)
    element = driver.find_element(by_type, identifier)
    element.clear()
    element.send_keys(value)
    haltStep()


def waitToLoad(driver, byType, identifier, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((byType, identifier))
    )


def haltStep():
    time.sleep(random.randint(1, 2))
