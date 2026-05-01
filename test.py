import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Get filename from Jenkins
test_file = os.getenv("TARGET_PHP_FILE", "index.php")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

try:
    url = f"http://localhost/staging/{test_file}"
    print(f"🚀 STRICT TESTING: {url}")
    
    driver.get(url)
    
    # Get content and page title
    content = driver.page_source.lower()
    page_title = driver.title.lower()

    # Red Flags: Added common PHP error strings and generic server error indicators
    errors = [
        "fatal error", "parse error", "warning:", 
        "stack trace:", "xdebug-error", "sqlsrv_query",
        "404 not found", "500 internal server error",
        "allowed memory size exhausted"
    ]
    
    found = [e for e in errors if e in content or e in page_title]
    
    # Strict Check 1: Content search
    if found:
        print(f"❌ ERROR DETECTED: {found}")
        sys.exit(1)

    # Strict Check 2: Check if the body is empty (often happens if display_errors is off)
    body_text = driver.find_element("tag name", "body").text.strip()
    if not body_text and "img" not in content:
        print("❌ ERROR: Page is blank! (Potential suppressed PHP Fatal Error)")
        sys.exit(1)

    print(f"✅ SUCCESS: {test_file} looks clean.")

except Exception as e:
    print(f"⚠️ TEST CRASHED: {e}")
    sys.exit(1)

finally:
    driver.quit()
