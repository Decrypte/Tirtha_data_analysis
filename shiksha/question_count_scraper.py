import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tqdm import tqdm
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# Suppressing SSL warnings
warnings.simplefilter("ignore", InsecureRequestWarning)

# Setup session with headers and proxy
session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
    }
)
proxy = {
    "http": "http://brd-customer-hl_a4a3b5b0-zone-youtube_rank:n4n7cvvboqyn@brd.superproxy.io:22225",
    "https": "http://brd-customer-hl_a4a3b5b0-zone-youtube_rank:n4n7cvvboqyn@brd.superproxy.io:22225",
}


def get_info(data):
    url, collegedunia_id = data
    max_attempts = 10
    attempts = 0
    while attempts < max_attempts:
        try:
            response = session.get(
                f"{url}/questions", proxies=proxy, verify=False, timeout=30
            )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                id_match = re.search(r"(\d+)$", url)
                shiksha_id = id_match.group(1) if id_match else "Not Found"
                result = {
                    "Collegedunia_id": collegedunia_id,
                    "Shiksha_id": shiksha_id,
                    "URL": url,
                    "College_Name": "Not Found",
                    "Q/A_Count": "Not Found",
                }
                breadcrumb_link = soup.select_one(
                    "div.breadcrumb3 a[href*='/college/']"
                )
                if breadcrumb_link:
                    result["College_Name"] = breadcrumb_link.get_text(strip=True)
                else:
                    title_tag = soup.find("title")
                    if title_tag:
                        name_match = re.search(r"^(.+?),", title_tag.text)
                        result["College_Name"] = (
                            name_match.group(1).strip() if name_match else "Not Found"
                        )
                meta_description = soup.find("meta", {"name": "Description"})
                if meta_description:
                    count_match = re.search(
                        r"See (\d+) Answered Questions",
                        meta_description.get("content", ""),
                    )
                    if count_match:
                        result["Q/A_Count"] = count_match.group(1)
                return result
            else:
                attempts += 1
                time.sleep(1)  # Simple linear backoff
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(f"Request failed on attempt {attempts+1} for {url}: {e}")
            attempts += 1
            time.sleep(1)  # Simple linear backoff
    return None


def fetch_all(data_pairs):
    results = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_data = {executor.submit(get_info, data): data for data in data_pairs}
        for future in tqdm(
            as_completed(future_to_data), total=len(data_pairs), desc="Processing URLs"
        ):
            result = future.result()
            if result:
                results.append(result)
            else:
                url, _ = future_to_data[future]
                print(f"Failed to process {url}")
    return results


# Load URLs and process them
df_urls = pd.read_csv("D:\\#Data\\Scraped Data\\ShikshaReveiwsData_April_2024.csv")
url_collegedunia_pairs = list(zip(df_urls["Url"], df_urls["Collegedunia_id"]))

results = fetch_all(url_collegedunia_pairs[:])

# Save results to CSV, ensuring all results are valid
if results:
    df_results = pd.DataFrame(results)
    csv_filename = "shiksha_colleges_question_count_april_2024_testing.csv"
    df_results.to_csv(f"D:\\#Data\\Scraped Data\\{csv_filename}", index=False)
    print(f"Data has been saved to {csv_filename}")
else:
    print("No results to save.")
