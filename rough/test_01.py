from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import warnings
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings("ignore")

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-infobars")  # Suppress infobars
options.add_argument("--disable-extensions")  # Disable extensions
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
options.add_argument(
    "--allow-running-insecure-content"
)  # Allow HTTPS content to be run from HTTP pages
options.add_argument(
    "--ignore-urlfetcher-cert-requests"
)  # Ignore certificate requests by URL fetcher
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-logging")  # This might help reduce logging
options.add_argument("--log-level=3")  # Set log level to only show severe
options.add_experimental_option(
    "excludeSwitches", ["enable-logging"]
)  # Suppress DevTools listening logs
options.add_argument("window-size=800x900")
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
            time.sleep(1)
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.sectional-faqs")
                    )
                )
            except Exception as e:
                print(f"Loading took too much time or an error occurred: {e}")
                return None
            faq_sections = driver.find_elements(By.CSS_SELECTOR, "div.sectional-faqs")
            if len(faq_sections) >= 3:
                print(f"{len(faq_sections)} number of FAQ sections found in the page.")
                break
        return driver.page_source


def extract_questions(html_content):
    if html_content is None:
        print("Failed to fetch HTML. No questions can be extracted.")
        return

    soup = BeautifulSoup(html_content, "html.parser")
    faq_sections = soup.select("div.sectional-faqs")

    all_questions = []
    for section in faq_sections:
        questions = section.select("strong span:nth-child(2)")
        for question_span in questions:
            all_questions.append(question_span.text.strip())

    print("Number of questions found:", len(all_questions))
    print(all_questions)


url = "https://www.shiksha.com/university/lpu-lovely-professional-university-jalandhar-28499/courses"
html = fetch_page_html(url)
if html:
    print("HTML fetched successfully")
    extract_questions(html)
else:
    print("Failed to fetch HTML")
