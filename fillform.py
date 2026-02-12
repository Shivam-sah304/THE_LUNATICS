import time, random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import undetected_chromedriver as uc

# ----------------- Main Function -----------------
def fillform(name, nmc_no, education):
    driver = setupDriver()
    driver.get("https://www.nmc.org.np/search-registered-doctor/")  # NMC search page

    # ---- Fill the form ----
    fill_input(driver, By.ID, "name", name)
    fill_input(driver, By.ID, "symbol", nmc_no)
    fill_input(driver, By.NAME, "degreed", education)

    # ---- Click the Search button ----
    waitToLoad(driver, By.XPATH, "//button[span[text()='Search']]")
    driver.find_element(By.XPATH, "//button[span[text()='Search']]").click()
    haltStep()

    # ---- Check if doctor exists ----
    try:
        # Wait for the result table
        waitToLoad(driver, By.CSS_SELECTOR, ".mt-5.col-md-6.col-lg-6.col-sm-12", timeout=5)
        # If we find the table, data is matched
        result = "yes"
    except:
        # Table not found → No result
        result = "no"

    # Close browser
    driver.quit()
    return result

# ----------------- Helper Functions -----------------
def fill_input(driver, by_type, identifier, value):
    waitToLoad(driver, by_type, identifier)
    element = driver.find_element(by_type, identifier)
    element.clear()
    element.send_keys(value)
    haltStep()

def setupDriver():
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def waitToLoad(driver, byType, identifier, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((byType, identifier))
    )

def haltStep():
    time.sleep(random.randint(1, 3))


# ----------------- Run -----------------
# result = fillform()
# print(result)  # It will print either "yes" or "no"