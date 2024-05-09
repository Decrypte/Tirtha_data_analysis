import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import warnings

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
    base_url = "https://www.shiksha.com/university/lpu-lovely-professional-university-jalandhar-28499/questions-{}?sort_by=relevance"
    url = base_url.format(page_num)
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return None


def extract_views(question_div):
    """Extract and process the views count from the given div element."""
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
        post_time = post_time_tag.get_text(strip=True) if post_time_tag else "N/A"

        question_tag = question_div.select_one(".dtl-qstn.col-head a")
        question_text = question_tag.get_text(strip=True) if question_tag else "N/A"

        views = extract_views(question_div)

        questions_data.append(
            {"question": question_text, "views": views, "posted": post_time}
        )

    return questions_data


def fetch_all_questions(start, end):
    all_questions = []
    for page in range(start, end + 1):
        html = fetch_page_html(page)
        if html:
            questions = extract_question_info(html)
            all_questions.extend(questions)
        time.sleep(1)
    return all_questions


start_page, end_page = 701, 800

all_questions_data = fetch_all_questions(start_page, end_page)
questions_df = pd.DataFrame(all_questions_data)
print(questions_df)
print(len(questions_df))


questions_df.to_csv("shiksha_lpu_questions_800.csv", index=False)
