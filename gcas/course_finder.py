from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import os
import time
from selenium.common.exceptions import TimeoutException
from data_extraction import get_data
from pagination import get_total_pages, iterate_pages
from checkpoint import save_checkpoint, load_checkpoint


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


driver = webdriver.Chrome(options=options)
driver.get("https://gcas.gujgov.edu.in/index.aspx#")
time.sleep(2)


def wait_for_element(xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def wait_for_clickable(xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))


q = wait_for_element('//*[@id="ContentPlaceHolder1_ddlAdmissionType"]')
elements = q.find_elements(By.TAG_NAME, 'option')

directory = "D:/#Data/Scraped Data/GCAS"
filename = "course_data.csv"
filepath = os.path.join(directory, filename)

if not os.path.exists(directory):
    os.makedirs(directory)

actions = ActionChains(driver)

state = load_checkpoint()
i_start, j_start, k_start = state['i'], state['j'], state['k']

for i in range(i_start, len(elements)):
    elements = wait_for_element('//*[@id="ContentPlaceHolder1_ddlAdmissionType"]').find_elements(By.TAG_NAME, 'option')
    c1_text = elements[i].text
    wait_for_clickable(f'//*[@id="ContentPlaceHolder1_ddlAdmissionType"]/option[{i+1}]').click()
    print(f"--{c1_text}")
    time.sleep(5)

    c_option = wait_for_element('//*[@id="ContentPlaceHolder1_ddlL2Search"]').find_elements(By.TAG_NAME, 'option')
    
    for j in range(j_start, len(c_option)):
        c_option = wait_for_element('//*[@id="ContentPlaceHolder1_ddlL2Search"]').find_elements(By.TAG_NAME, 'option')
        c2_text = c_option[j].text
        wait_for_clickable(f'//*[@id="ContentPlaceHolder1_ddlL2Search"]/option[{j+1}]').click()
        print(f"-------------{c2_text}")
        time.sleep(5)
        
        branch = wait_for_element('//*[@id="ContentPlaceHolder1_ddlAdmission"]').find_elements(By.TAG_NAME, 'option')
        
        for k in range(k_start, len(branch)):
            branch = wait_for_element('//*[@id="ContentPlaceHolder1_ddlAdmission"]').find_elements(By.TAG_NAME, 'option')
            c3_text = branch[k].text
            wait_for_clickable(f'//*[@id="ContentPlaceHolder1_ddlAdmission"]/option[{k+1}]').click()
            print(f"------------------------{c3_text}")
            time.sleep(5)

            search_button = wait_for_clickable('//input[@value="Search"]')

            driver.execute_script("window.scrollTo(0, 0);")
            actions.move_to_element(search_button).perform()
            time.sleep(1)

            try:
                search_button.click()
            except Exception as e:
                print(f"Click intercepted, retrying: {e}")
                driver.execute_script("arguments[0].scrollIntoView();", search_button)
                actions.move_to_element(search_button).perform()
                wait_for_clickable('//input[@value="Search"]').click()

            try:
                wait_for_element('//div[@id="example1_wrapper"]', timeout=10)
            except TimeoutException:
                continue

            html_content = driver.page_source
            total_pages = get_total_pages(driver)
            result = iterate_pages(driver, total_pages, c1_text, c2_text, c3_text)

            if result:
                if not os.path.isfile(filepath):
                    df = pd.DataFrame(result)
                    df.to_csv(filepath, index=False)
                else:
                    df = pd.DataFrame(result)
                    df.to_csv(filepath, mode='a', header=False, index=False)

            save_checkpoint({'i': i, 'j': j, 'k': k + 1})

        k_start = 1

    j_start = 1

driver.quit()
