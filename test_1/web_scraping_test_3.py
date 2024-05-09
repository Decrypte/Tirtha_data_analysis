from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import warnings
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


warnings.filterwarnings("ignore")

# Selenium setup
options = Options()
options.add_argument("--headless")
options.add_argument("window-size=800x900")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
)


def fetch_page_html(url):
    with webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    ) as driver:
        driver.get(url)

        # Enhanced scrolling & wait for sections to appear
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolling the page.")
            time.sleep(1)

            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.sectional-faqs")
                    )
                )
                print("Element found, waiting for FAQ sections.")
            except Exception as e:
                print(f"Loading took too much time or an error occurred: {e}")
                return None

            faq_sections = driver.find_elements(By.CSS_SELECTOR, "div.sectional-faqs")
            if len(faq_sections) >= 5:
                print(f"Success! {len(faq_sections)} number of FAQ sections found.")
                break

        print("Retrieving HTML source.")
        return driver.page_source


def extract_questions(html_content):
    if html_content is None:
        print("Failed to fetch HTML. No questions can be extracted.")
        return

    soup = BeautifulSoup(html_content, "html.parser")

    questions_dict = {}
    headings = []
    all_questions = []

    section_headings = soup.select("div._5977 h5 div")
    for heading in section_headings:
        headings.append(heading.text.strip()[3:])

    faq_sections = soup.select("div.sectional-faqs")
    for section in faq_sections:
        questions = section.select("strong span:nth-child(2)")
        section_questions = []
        for question_span in questions:
            section_questions.append(question_span.text.strip())
        all_questions.append(section_questions)

    # print("Number of questions found:", len(all_questions))

    if len(headings) != len(all_questions):
        print(
            "Mismatch between the number of headings and the number of question lists."
        )
    else:
        # Create and print the dictionary if everything matches
        questions_dict = dict(zip(headings, all_questions))
        print("Extracted Questions Dictionary:")
        for key, value in questions_dict.items():
            print(f"{key}: {value}")


url = "https://www.shiksha.com/university/lpu-lovely-professional-university-jalandhar-28499"
html = fetch_page_html(url)
if html:
    print("HTML fetched successfully")
    extract_questions(html)
else:
    print("Failed to fetch HTML")

# url_paths_type_1 = ["courses", "admission", "cutoff"]
# url_paths_type_2 = ["reviews", "placements", "infrastructure", "scholarships"]
# url_paths_type_3 = ["ranking", "infrastructure", "scholarships"]
