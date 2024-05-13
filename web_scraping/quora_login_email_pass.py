from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def setup_driver():
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=webdriver.ChromeOptions())


def login_to_quora(driver, email, password):
    driver.get("https://www.quora.com/login")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "email"))
    ).send_keys(email)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "password"))
    ).send_keys(password)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button//div[contains(text(), "Login")]')
        )
    ).click()
    time.sleep(5)  # Wait for the main page to load after login


def search_quora(driver, query):
    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='text'][placeholder='Search Quora']")
        )
    )
    search_input.send_keys(query)
    time.sleep(1)
    search_input.send_keys(Keys.ENTER)
    print("Search performed.")


def main(email, password, query):
    driver = setup_driver()
    try:
        login_to_quora(driver, email, password)
        search_quora(driver, query)
        time.sleep(15)
    finally:
        driver.quit()
        print("Driver session terminated.")


if __name__ == "__main__":
    email = "tsn8bits@gmail.com"
    password = "Password@123"
    query = "Web scraping ideas"
    main(email, password, query)
