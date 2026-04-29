from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("file:///var/www/html/index.html")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "title"))
    )

    title = driver.find_element(By.ID, "title").text

    assert title == "Hello CI/CD", f"Expected 'Hello CI/CD' but got '{title}'"

    print("TEST PASSED")

except Exception as e:
    print("TEST FAILED:", e)

finally:
    driver.quit()

