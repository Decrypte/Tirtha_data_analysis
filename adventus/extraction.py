from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re


def get_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    courses_data = []  # List to store all courses' information

    # Find all course card bodies
    course_cards = soup.find_all("div", class_="course-card-wrapper")

    for card in course_cards:
        # Extract course name
        title_element = card.find("a", class_="course-card__title")
        course_link = f"https://app.adventus.io{title_element.get("href")}"
        match = re.search(r"/course/(\d+)", course_link)
        if match:
            course_id = match.group(1)
        course_name = title_element.text.strip() if title_element else ""

        # Extract college, location, duration, fees, and intakes
        info_items = card.find_all("span", class_="course-card__course-info__text")

        college_name = info_items[0].text.strip() if len(info_items) > 0 else ""
        location = info_items[1].text.strip() if len(info_items) > 1 else ""
        duration = (
            info_items[2].text.strip()
            if len(info_items) > 2 and "year" in info_items[2].text
            else ""
        )

        # Handle optional turnaround time
        fee_index = 3
        if len(info_items) > 4 and "days" in info_items[4].text:
            turnaround_time = info_items[4].text.strip()
            fee_index = 5
        else:
            turnaround_time = ""

        fees = (
            info_items[fee_index].text.strip()
            if len(info_items) > fee_index
            and any(
                kw in info_items[fee_index].text for kw in ["per year", "per course"]
            )
            else ""
        )

        # Extract intake information
        intake_element = card.find("span", class_="intake-section__text-intake")
        intakes = intake_element.text.strip() if intake_element else ""

        # Collect all the information in a dictionary
        course_info = {
            "course_id": course_id,
            "course_name": course_name,
            "course_url": course_link,
            "college": college_name,
            "location": location,
            "duration": duration,
            "turnaround_time": turnaround_time,
            "fees": fees,
            "intakes": intakes,
        }

        # Append the course information dictionary to the list
        courses_data.append(course_info)

    return courses_data


def page_change(driver):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pagination_section = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "pagination"))
        )

        current_page = pagination_section.find_element(
            By.CSS_SELECTOR, "li.page-item.active"
        )
        next_page = current_page.find_elements(
            By.XPATH, "following-sibling::li[not(@class='disabled')]"
        )

        if next_page:  # Check if any "next" button was found
            next_page_link = next_page[0].find_element(By.TAG_NAME, "a")
            next_page_link.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "course-card__body")
                )
            )
            return True
        else:
            print("No more pages to navigate.")
            return False
    except Exception as e:
        print(f"Error in page navigation: {e}")
        return False
