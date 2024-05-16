import pandas as pd
import numpy as np
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from login_adventus import login_adventus
from adventus.data_extraction import full_course_info
from utils import config

import warnings
warnings.filterwarnings("ignore")


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    login_adventus(driver, config.email, config.password)
    url = "https://app.adventus.io/course/58932"
    driver.get(url)
    
                
    html_content = driver.page_source
    course_data = full_course_info(html_content, url)
    driver.quit()

    print(course_data)
