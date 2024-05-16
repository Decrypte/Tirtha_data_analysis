import pandas as pd
import numpy as np
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from login_adventus import login_adventus
from adventus.data_extraction import full_course_info
from utils import config
import time
import random
import warnings
warnings.filterwarnings("ignore")


def save_data_batch(all_data, filename):
    data = pd.DataFrame(all_data)
    data.replace("", np.nan, inplace=True)
    data.dropna(how="all", inplace=True)

    data.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)
    # print(f"Batch appended to {filename}.")


if __name__ == "__main__":
    df_urls = pd.read_csv("D:\\#Data\\Scraped Data\\Adventus\\Final\\adventus_india_data.csv")
    urls = df_urls["course_url"].tolist()

    filename = "D:\\#Data\\Scraped Data\\Adventus\\Final\\Course_data.csv"

    # Set up Chrome options
    # options = Options()
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)

    # Headers
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     "Accept-Language": "en-US,en;q=0.9",
    # }
    # for key, value in headers.items():
    #     options.add_argument(f'--header={key}:{value}')

    # # Proxy
    # proxy = {
    #     "http": "http://brd-customer-hl_a4a3b5b0-zone-youtube_rank:n4n7cvvboqyn@brd.superproxy.io:22225",
    #     "https": "http://brd-customer-hl_a4a3b5b0-zone-youtube_rank:n4n7cvvboqyn@brd.superproxy.io:22225",
    # }
    # options.add_argument(f'--proxy-server={proxy["http"]}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))    
    batch_size = 100
    all_data = []

    try:
        login_adventus(driver, config.email, config.password) # login once first
        time.sleep(random.uniform(2, 5))
        driver.get(urls[0]) # forcing out notification on first search
        
        for url in tqdm(urls[1300:]):
            try:
                driver.get(url)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "lumos-header")))
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "tab-particulars")))
                
                html_content = driver.page_source
                course_data = full_course_info(html_content, url)

                if course_data:
                    all_data.append(course_data)

                if len(all_data) >= batch_size:
                    save_data_batch(all_data, filename)     # batch wise data saved
                    all_data = [] 

            except Exception as e:
                print(f"Error fetching {url}: {str(e)}")
                continue                                    # if url current fetching error then next url
    
    except Exception as e:
        print(str(e))
    
    finally:
        driver.quit()
