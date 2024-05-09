from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def setup_driver():
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    options.add_argument("--window-size=500x800")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-browser-side-navigation")
    # options.add_argument("--hide-scrollbars")
    # options.add_argument("--enable-logging")
    # options.add_argument("--log-level=0")
    # options.add_argument("--v=99")
    # options.add_argument("--single-process")
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--homedir=/tmp")
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    # )
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def login_to_quora(driver, email):
    driver.get("https://www.quora.com/")
    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".puppeteer_test_login_button_google")
            )
        ).click()
        print("Clicked on the Google login button.")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "identifierId"))
        ).send_keys(email)
        print("Email entered.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Next']/parent::button")
            )
        ).click()
        print("Clicked on the Next button.")
        time.sleep(10)

        # Additional steps for handling password can be added here

    except Exception as e:
        print(f"An error occurred during Google login: {e}")
        # traceback.print_exc()

    finally:
        # Handle window switch back if needed
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[0])
            print("Switched back to the original window.")


def main(email):
    driver = setup_driver()
    try:
        login_to_quora(driver, email)
    finally:
        driver.quit()
        print("Driver quit.")


if __name__ == "__main__":
    email = "tsn8bits@gmail.com"
    main(email)
