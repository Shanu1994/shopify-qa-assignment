import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import traceback

# ==========================================
# CONFIGURATION
# ==========================================

AdNabuTestStore_URL = "https://adnabu-store-assignment1.myshopify.com/"
Website_PASSWORD = "AdNabuQA"
WAIT_TIME = 15

# ==========================================
# DRIVER SETUP
# ==========================================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

wait = WebDriverWait(driver, WAIT_TIME)

try:

    # ==========================================
    # OPEN WEBSITE
    # ==========================================

    driver.get(AdNabuTestStore_URL)

    print("Website opened successfully")

    # ==========================================
    # HANDLE PASSWORD PAGE
    # ==========================================

    try:

        password_input = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "password")
            )
        )

        password_input.clear()
        password_input.send_keys(Website_PASSWORD)

        print("Password entered")

        submit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit']")
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            submit_button
        )

        print("Submit button clicked")

        wait.until(
            EC.invisibility_of_element_located(
                (By.NAME, "password")
            )
        )

        print("Successfully entered store")

        driver.get(AdNabuTestStore_URL)

    except TimeoutException:
        print("Password page not found")

    # ==========================================
    # GET ALL PRODUCT LINKS
    # ==========================================

    product_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//a[contains(@href,'/products/')]")
        )
    )

    product_links = []

    for item in product_elements:

        href = item.get_attribute("href")

        if href and href not in product_links:
            product_links.append(href)

    print(f"Total Product Links Found: {len(product_links)}")

    product_added = False

    # ==========================================
    # LOOP THROUGH PRODUCTS
    # ==========================================

    for product_url in product_links:

        print(f"\nOpening Product URL: {product_url}")

        driver.get(product_url)

        try:

            # Wait for product page

            wait.until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "body")
                )
            )

            print("Product page opened")

            # ==========================================
            # SELECT VARIANT IF AVAILABLE
            # ==========================================
            
            try:

                variant_option = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "(//input[@type='radio'])[1]")
                    )
                )

                driver.execute_script(
                    "arguments[0].click();",
                    variant_option
                )

                print("Variant selected")

            except TimeoutException:
                print("No variant option found")

            # ==========================================
            # FIND ADD TO CART BUTTON
            # ==========================================
            
            add_to_cart_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart')]"
                    )
                )
            )

            driver.execute_script(
                "arguments[0].click();",
                add_to_cart_button
            )

            print("Add To Cart clicked successfully")

            product_added = True

            break

        except TimeoutException:
            print("Add To Cart not available for this product")

    # ==========================================
    # FINAL VALIDATION
    # ==========================================
    
    if product_added:

    # ==========================================
    # CREATE SCREENSHOT FOLDER
    # ==========================================

        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    # ==========================================
    # SAVE SUCCESS SCREENSHOT
    # ==========================================

        driver.save_screenshot(
            "screenshots/test_passed.png"
        )

        print("Success screenshot saved")

        print("\n===================================")
        print("TEST PASSED")
        print("Variant Selection + Add To Cart Successful")
        print("===================================")

    else:
        raise Exception("No purchasable product found")

except Exception as e:

    print("\n===================================")
    print("TEST FAILED")
    print("ERROR:", str(e))
    print("===================================")

    traceback.print_exc()

    # ==========================================
    # SAVE FAILURE SCREENSHOT
    # ==========================================

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    driver.save_screenshot(
        "screenshots/failure_screenshot.png"
    )

    print("Screenshot saved as failure_screenshot.png")

finally:
    driver.quit()