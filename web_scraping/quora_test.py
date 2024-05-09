import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# WebDriver setup function
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=800,1000")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )


# Function to log into Quora
def login_to_quora(driver, username, password, use_google_login=True):
    driver.get("https://www.quora.com/")
    try:
        if use_google_login:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[text()="Continue with Google"]')
                )
            ).click()
            # handle the Google login process
            # waiting for new elements to appear in a new window or frame
            # Handle the login details in the new window or tab
            time.sleep(5)  # Placeholder for actual login handling
        else:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="email"]'))
            ).send_keys(username)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
            ).send_keys(password)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button//div[contains(text(), "Login")]')
                )
            ).click()

        time.sleep(5)  # Wait for the login process to complete

    except Exception as e:
        print("An error occurred during login:", e)


def main():
    driver = setup_driver()
    login_to_quora(driver, None, None, True)
    driver.quit()
    # try:
    #     login_method = input(
    #         "Choose login method (1 for email/password, 2 for Google): "
    #     )
    #     if login_method == "2":
    #         login_to_quora(driver, None, None, use_google_login=True)
    #     else:
    #         username = input("Enter email: ")
    #         password = getpass("Enter password: ")
    #         login_to_quora(driver, username, password)
    # finally:
    #     driver.quit()


if __name__ == "__main__":
    main()
