from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

options = Options()

# ✅ Required for Jenkins / Ubuntu 24
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

# ✅ Extra stability (important in CI)
options.add_argument("--window-size=1920,1080")
options.add_argument("--remote-debugging-port=9222")

service = Service("/usr/bin/chromedriver")

driver = None

try:
    print("Starting ChromeDriver...")

    driver = webdriver.Chrome(service=service, options=options)

    print("Opening page...")
    driver.get("file:///var/www/html/index.html")

    print("Waiting for element...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "title"))
    )

    title = driver.find_element(By.ID, "title").text
    print("Found title:", title)

    assert title == "Hello CI/CD", f"Expected 'Hello CI/CD' but got '{title}'"

    print("TEST PASSED")

except Exception as e:
    print("TEST FAILED")
    print("Error:", e)
    traceback.print_exc()
    raise   # 🔥 ensures Jenkins marks build as FAILED

finally:
    if driver:
        driver.quit()
        print("Browser closed")
