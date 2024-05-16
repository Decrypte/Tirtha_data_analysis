import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import warnings
from tqdm import tqdm

warnings.filterwarnings("ignore")

proxy = {
    "http": "http://brd-customer-hl_a4a3b5b0-zone-youtube_rank:n4n7cvvboqyn@brd.superproxy.io:22225",
    "https": "http://brd-customer-hl_a4a3b5b0-zone-youtube_rank:n4n7cvvboqyn@brd.superproxy.io:22225",
}

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# }

session = requests.Session()
# session.headers.update(headers)
session.proxies.update(proxy)
session.verify = False

def fetch_page_html(page_num):
    base_url = "https://www.shiksha.com/university/bits-pilani-birla-institute-of-technology-and-science-467/questions-{}?sort_by=relevance"
    url = base_url.format(page_num)
    try:
        response = session.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except requests.RequestException as e:
        # print(f"Error fetching page {page_num}: {e}")
        return None

def extract_views(question_div):
    viewers_spans = question_div.select("div.right-cl span.viewers-span")
    views = ""

    for span in viewers_spans:
        text = span.get_text(strip=True)
        if "Views" in text:
            numeric_text = text.replace(" Views", "").strip()

            match = re.match(r"(\d+(\.\d+)?)([km]?)", numeric_text, re.IGNORECASE)
            if match:
                number = float(match.group(1))
                suffix = match.group(3).lower()

                if suffix == "k":
                    views = str(int(number * 1000))
                elif suffix == "m":
                    views = str(int(number * 1000000))
                else:
                    views = str(int(number))
            else:
                views = numeric_text

            break

    return views

def extract_question_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    questions_data = []

    question_divs = soup.select("div[questionid]")
    if not question_divs:
        return []

    for question_div in question_divs:
        post_time_tag = question_div.select_one(".dtl-qstn.col-head span")
        post_time = post_time_tag.get_text(strip=True) if post_time_tag else ""

        question_tag = question_div.select_one(".dtl-qstn.col-head a")
        question_text = question_tag.get_text(strip=True) if question_tag else ""

        views = extract_views(question_div)

        questions_data.append(
            {"question": question_text, "views": views, "posted": post_time}
        )

    return questions_data

def fetch_all_questions(start, end, batch_size, save_path):
    all_questions = []
    for page in tqdm(range(start, end + 1)):
        html = fetch_page_html(page)
        if html:
            questions = extract_question_info(html)
            if questions:
                all_questions.extend(questions)
        
        # Saving data in batches
        if (page - start + 1) % batch_size == 0:
            save_data_batch(all_questions, save_path)
            all_questions = []

        time.sleep(1)
    
    # Save any remaining data
    if all_questions:
        save_data_batch(all_questions, save_path)

def save_data_batch(data, save_path):
    df = pd.DataFrame(data)
    with open(save_path, 'a', newline='', encoding='utf-8') as f:
        df.to_csv(f, index=False, header=f.tell() == 0)

start_page, end_page = 1, 400
batch_size = 20
directory = "D://#Data//Scraped Data//Shiksha"
filename = "bits_pilani.csv"

fetch_all_questions(start_page, end_page, batch_size, f"{directory}//{filename}")
