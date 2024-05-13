from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def handle_notification(driver):
    try:
        notification_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Skip")]'))
        )
        notification_button.click()
    except Exception as e:
        print(e)


def handle_ad(driver):
    try:
        # Wait for the ad's close button to be clickable
        close_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="container"]//svg'))
        )
        # Click the close button
        close_button.click()
    except Exception as e:
        print(f"Failed to close the ad: {e}")
