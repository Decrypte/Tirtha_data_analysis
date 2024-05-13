import pandas as pd
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    )
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install(), log_path=os.devnull)
    return webdriver.Chrome(service=service, options=options)


def get_info(url):
    driver = setup_driver()
    driver.get(f"{url}/questions")

    # Extract the ID from the URL using regex
    id_match = re.search(r"(\d+)$", url)  # Regex to find digits at the end of the URL
    university_id = id_match.group(1) if id_match else "Not Found"

    data = {
        "University_ID": university_id,
        "URL": url,
        "College_Name": "Not Found",
        "Q/A_Count": "Not Found",
    }

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "meta"))
        )
        title_text = driver.title
        name_match = re.search(r"^(.+?),", title_text)  # Match up to the first comma
        if name_match:
            data["College_Name"] = name_match.group(1).strip()

        meta_description = driver.find_element(By.NAME, "Description").get_attribute(
            "content"
        )
        count_match = re.search(r"See (\d+) Answered Questions", meta_description)
        if count_match:
            data["Q/A_Count"] = count_match.group(1)

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

    return data


# Read the dataset
df_urls = pd.read_csv("D:\\#Data\\Scraped Data\\ShikshaReveiwsData_April_2024.csv")
urls = df_urls["Url"]

# Collect data for all URLs
results = [get_info(url) for url in urls[:3]]

df_results = pd.DataFrame(results)
csv_filename = "shiksha_colleges_question_count_Apr_2024.csv"
df_results.to_csv(f"D:\\#Data\\Scraped Data\\{csv_filename}", index=False)
print(f"Data has been saved to {csv_filename}")
