from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import numpy as np
from utils import config, helpers
from login_adventus import login_adventus
from adventus.data_extraction import get_info, page_change


def navigate_to_course_finder(driver):
    # Navigate to the 'Course Search' page
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "adv-side-nav"))
    )
    course_search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/course-search']"))
    )
    course_search_button.click()

    helpers.handle_notification(driver)


def find_colleges(driver, state_to_select):
    try:
        print("Waiting for the page to fully load...")
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        dropdown_trigger_country = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'spotlight-nationality-wrapper')]//div[@role='combobox']",
                )
            )
        )
        dropdown_trigger_country.click()

        time.sleep(1)

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='adv-search-dropdown__search-wrapper']//input")
            )
        )
        search_input.send_keys("India")

        india_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@data-option='India']"))
        )
        india_option.click()

        time.sleep(2)

        spotlight_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='adv-content-wrapper spotlight-nationality-wrapper']",
                )
            )
        )

        state_dropdown = spotlight_container.find_element(
            By.XPATH,
            ".//div[contains(@class, 'adv-search-dropdown')][2]//div[@class='adv-search-dropdown-selection']",
        )

        state_dropdown.click()

        state_to_select = config.states[0]

        state_search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='adv-search-dropdown'][2]//input")
            )
        )
        state_search_input.send_keys(state_to_select)
        print(f"Entered state name in search: {state_to_select}")

        # Select the state from the dropdown
        selected_state_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[@data-option='{state_to_select}']")
            )
        )
        selected_state_option.click()
        print(f"State selected: {state_to_select}")

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'page-count-container-step') and contains(text(), '100')]",
                )
            )
        ).click()

        time.sleep(5)

    except Exception as e:
        import traceback

        print(f"Error during interaction with the course search form: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        login_adventus(driver, config.email, config.password)
        for state in config.states[:]:  # Adjust according to your needs
            navigate_to_course_finder(driver)
            find_colleges(driver, state)

            all_data = []
            while True:
                current_html = driver.page_source
                page_data = get_info(current_html, state)
                if page_data:
                    all_data.extend(page_data)
                    print("Data extracted from current page.")
                else:
                    print("No data found on current page.")

                if not page_change(driver):
                    break

            if all_data:
                data = pd.DataFrame(all_data)
                data.replace("", np.nan, inplace=True)
                data.dropna(how="all", inplace=True)
                filename = f"{state} Data.csv"
                data.to_csv(f"D:\\#Data\\Scraped Data\\Adventus\\{filename}", index=False)
                print("Data saved.")
            else:
                print("No scraped data to save.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
