import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Create a requests session to handle cookies and persist headers
session = requests.Session()
session.headers.update(headers)


def fetch_page_html(page_num):
    base_url = "https://www.shiksha.com/university/lpu-lovely-professional-university-jalandhar-28499/questions-{}?sort_by=relevance"
    url = base_url.format(page_num)
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an error for any HTTP errors
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return None


def extract_question_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    questions_data = []

    for question_div in soup.select("div[questionid]"):
        # post time from the <span>
        post_time_tag = question_div.select_one(".dtl-qstn.col-head span")
        post_time = post_time_tag.get_text(strip=True) if post_time_tag else "N/A"

        # question text
        question_tag = question_div.select_one(".dtl-qstn.col-head a")
        question_text = question_tag.get_text(strip=True) if question_tag else "N/A"

        # views count
        viewers_spans = question_div.select("div.right-cl span.viewers-span")
        views = "N/A"  # Default value

        for span in viewers_spans:
            text = span.get_text(strip=True)
            if "Views" in text:
                views = text
                break

        questions_data.append(
            {"question": question_text, "views": views, "posted": post_time}
        )

    return questions_data


def fetch_all_questions(pages):
    all_questions = []
    for page in range(1, pages + 1):
        html = fetch_page_html(page)
        if html:
            questions = extract_question_info(html)
            all_questions.extend(questions)
        time.sleep(2)
    return all_questions


num_pages = 93

all_questions_data = fetch_all_questions(num_pages)
questions_df = pd.DataFrame(all_questions_data)
print(questions_df)

questions_df.to_csv("questions_data.csv", index=False)
