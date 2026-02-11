import time, random, re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import undetected_chromedriver as uc


# ----------------- Main Function -----------------
def fillform(name="Neeta Timilsina", nmc_no=13039, education="MBBS"):
    driver = setupDriver()
    driver.get("https://www.nmc.org.np/search-registered-doctor/")

    # ---- Fill the form ----
    fill_input(driver, By.ID, "name", name)
    fill_input(driver, By.ID, "symbol", str(nmc_no))  # ensure string
    fill_input(driver, By.NAME, "degreed", education)

    # ---- Click the Search button ----
    waitToLoad(driver, By.XPATH, "//button[span[text()='Search']]")
    driver.find_element(By.XPATH, "//button[span[text()='Search']]").click()
    haltStep()

    # ---- Extract the result ----
    results_list = []

    try:
        waitToLoad(driver, By.CSS_SELECTOR, ".mt-5.col-md-6.col-lg-6.col-sm-12")
        result_table = driver.find_element(
            By.CSS_SELECTOR, ".mt-5.col-md-6.col-lg-6.col-sm-12"
        )

        lines = result_table.text.split("\n")

        for i in range(len(lines)):
            key = lines[i].strip()
            results_list.append(key)

    except Exception:
        try:
            no_result_text = driver.find_element(
                By.XPATH, "//*[contains(text(), 'No result')]"
            ).text
            results_list = no_result_text
        except Exception:
            results_list = "Could not fetch results"

    time.sleep(3)

    try:
        driver.quit()
    except:
        pass

    return results_list


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
result = fillform()

print('---')
print(result)
print('-----')

result_dict = {}

for item in result:
    pass
