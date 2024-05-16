from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from data_extraction import get_data


def get_total_pages(driver):
    try:
        pagination_element = driver.find_element(By.ID, "example1_paginate")
        last_page_element = pagination_element.find_elements(By.TAG_NAME, 'a')
        if len(last_page_element) > 1:
            total_pages = int(last_page_element[-2].text)
        else:
            total_pages = 1
    except Exception:
        total_pages = 1
    return total_pages


def iterate_pages(driver, total_pages, c1, c2, c3):
    all_data = []
    actions = ActionChains(driver)
    for page in range(1, total_pages + 1):
        html_content = driver.page_source
        page_data = get_data(html_content, c1, c2, c3)
        all_data.extend(page_data)
        try:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "example1_next")))
            if "disabled" not in next_button.get_attribute("class"):
                actions.move_to_element(next_button).perform()
                time.sleep(1)
                next_button.click()
                time.sleep(2)
            else:
                break
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    return all_data
