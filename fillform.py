import time, random, re
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
    fill_input(driver, By.ID, "name", name)        # Full Name
    fill_input(driver, By.ID, "symbol", nmc_no)              # NMC No
    fill_input(driver, By.NAME, "degreed", education)         # Degree

    # ---- Click the Search button ----
    waitToLoad(driver, By.XPATH, "//button[span[text()='Search']]")
    driver.find_element(By.XPATH, "//button[span[text()='Search']]").click()
    haltStep()

    # ---- Extract the result ----
    results_list = []
    try:
        # Wait for the result table
        waitToLoad(driver, By.CSS_SELECTOR, ".mt-5.col-md-6.col-lg-6.col-sm-12")
        result_table = driver.find_element(By.CSS_SELECTOR, ".mt-5.col-md-6.col-lg-6.col-sm-12")
        # Split text by lines and parse key-value pairs
        lines = result_table.text.split("\n")
        for i in range(0, len(lines), 1):
            key = lines[i].strip()
            # value = lines[i + 1].strip() if i + 1 < len(lines) else ""
            # results_dict[key] = value
            results_list.append(key)
    except:
        # If table not found, maybe 'No result found' is displayed
        try:
            no_result_text = driver.find_element(By.XPATH, "//*[contains(text(), 'No result')]").text
            results_list = no_result_text
        except:
            results_list = "Could not fetch results"

    # Keep browser open briefly so you can see it
    time.sleep(3)
    driver.quit()
    
    return results_list

# ----------------- Helper Functions -----------------
def fill_input(driver, by_type, identifier, value):
    waitToLoad(driver, by_type, identifier)
    element = driver.find_element(by_type, identifier)
    element.clear()  # Clear field before typing
    element.send_keys(value)
    haltStep()

def setupDriver():
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--start-maximized")
    
    # Specify Brave browser path
    options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    
    # Auto-download matching driver
    driver = uc.Chrome(version_main=144, options=options)  # Update version_main to match Brave version
    
    # Stealth: hide webdriver property
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.implicitly_wait(10)
    return driver

def waitToLoad(driver, byType, identifier, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((byType, identifier))
    )

def haltStep():
    time.sleep(random.randint(1, 3))



result = fillform()
print('---')
print(result)
print('-----')

result_dict = {}

for list in result:
    pass