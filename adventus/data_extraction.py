from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re


def get_info(html_content, state):
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
            "state": state,
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
        pagination_section = WebDriverWait(driver, 20).until(
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
            WebDriverWait(driver, 20).until(
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


def full_course_info(html_content, url):
    soup = BeautifulSoup(html_content, "html.parser")

    header_content = soup.find("div", class_="lumos-header__content")
    course_name = header_content.find("h1", class_="lumos-header__heading").text.strip() if header_content else ""
    college_location = header_content.find("p", class_="lumos-header__subheading").text.strip() if header_content else ""
    
    if ", " in college_location:
        split_loc = college_location.split(", ", 1)
        college = split_loc[0]
        location = split_loc[1]
    else:
        college = college_location
        location = ""

    particulars = soup.find("div", id="tab-particulars")
    course_data = {}

    if particulars:
        details = particulars.find_all(["dt", "dd"])
        detail_dict = {details[i].text.strip(): details[i + 1].text.strip() for i in range(0, len(details) - 1, 2)}

        course_data = {
            "course_name": course_name,
            "url": url,
            "college": college,
            "location": location,
            "official_link": details[1].a['href'] if details[1].find('a') else "",  # first 'dd' after 'Name' contains link
            "level": detail_dict.get("Level", ""),
            "course_code": detail_dict.get("Course Code", ""),
            "duration": detail_dict.get("Duration", ""),
            "mode": detail_dict.get("Delivery", ""),
            "currency": detail_dict.get("Currency", ""),
            "tuition_fee": detail_dict.get("Tuition Fee", ""),
            "appl_fee": detail_dict.get("Application Fee", ""),
            "language": detail_dict.get("Language of Tuition", ""),
            "major_specialization": detail_dict.get("Major / Specialisation", "")
        }

    return course_data