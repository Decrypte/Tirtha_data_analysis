from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from utils import config, helpers


email = config.email
password = config.password


def login_adventus(driver, email, password):
    driver.get("https://app.adventus.io/admin/login")

    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # Ensure all masks are removed to make the inputs interactable
    driver.execute_script(
        "document.querySelectorAll('.adv-inputv2-mask').forEach(el => el.style.display = 'block');"
    )

    # Setting the values of email and password fields directly using JavaScript
    driver.execute_script(
        f"document.querySelector('input[name=\"email\"]').value = '{email}';"
    )
    driver.execute_script(
        f"document.querySelector('input[name=\"password\"]').value = '{password}';"
    )

    # Triggering change events to simulate user interactions
    driver.execute_script(
        "document.querySelector('input[name=\"email\"]').dispatchEvent(new Event('change', { 'bubbles': true }));"
    )
    driver.execute_script(
        "document.querySelector('input[name=\"password\"]').dispatchEvent(new Event('change', { 'bubbles': true }));"
    )

    # Click the login button
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Log in")]'))
    )
    login_button.click()
    helpers.handle_notification(driver)


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        login_adventus(driver, email, password)
        helpers.handle_notification(driver)
        time.sleep(5)
        #  Pass control to the course finder script (which you'll create next)
        #  Example: import course_finder; course_finder.run(driver)
    finally:
        driver.quit()
