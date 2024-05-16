from bs4 import BeautifulSoup


def get_data(html_content, c1, c2, c3):
    soup = BeautifulSoup(html_content, "html.parser")
    data = []
    course_type, course_domain, course_sub_domain = c1, c2, c3
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        
        university = cols[1].get_text(strip=True)
        college = cols[2].get_text(strip=True)
        course_name = cols[3].get_text(strip=True)
        subject = cols[4].get_text(strip=True)
        col_type = cols[5].get_text(strip=True)
        medium = cols[6].get_text(strip=True)
        shift = cols[7].get_text(strip=True)
        system = cols[8].get_text(strip=True)
        status = cols[9].find('span').get_text(strip=True)

        data.append({
            "Course type": course_type,
            "Course domain": course_domain,
            "Course sub-domain": course_sub_domain,
            "University": university,
            "College": college,
            "Course Name": course_name,
            "Subject Name": subject,
            "College Type": col_type,
            "Medium": medium,
            "Shift": shift,
            "Education system": system,
            "Hostel availability": status
        })

    return data

