import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

test_file = os.getenv("TARGET_PHP_FILE", "index.php")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

try:
    url = f"http://localhost/staging/{test_file}"
    print(f"🧐 Auditing: {url}")
    
    driver.get(url)
    content = driver.page_source.lower()

    # 🚩 FLAG 1: Explicit PHP Errors
    errors = ["fatal error", "parse error", "warning:", "stack trace:"]
    found_errors = [e for e in errors if e in content]
    
    # 🚩 FLAG 2: Check if the specific expected output is MISSING
    # If the PHP crashed, "hello world" won't be in the source
    expected_text = "hello world"
    
    if found_errors:
        print(f"❌ BLOCKED: Found PHP errors: {found_errors}")
        sys.exit(1)
        
    if expected_text not in content:
        print(f"❌ BLOCKED: PHP crashed or failed to render expected output ('{expected_text}').")
        # We print the content to Jenkins logs so you can see what happened
        print("--- PAGE CONTENT START ---")
        print(driver.page_source)
        print("--- PAGE CONTENT END ---")
        sys.exit(1)

    print(f"✅ PASS: {test_file} rendered correctly.")

except Exception as e:
    print(f"⚠️ TEST SYSTEM FAILURE: {e}")
    sys.exit(1)
finally:
    driver.quit()
