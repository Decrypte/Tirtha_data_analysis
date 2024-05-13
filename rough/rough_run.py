# import requests
# import re
# from bs4 import BeautifulSoup
# import warnings
# from urllib3.exceptions import InsecureRequestWarning

# warnings.simplefilter("ignore", InsecureRequestWarning)

# session = requests.Session()
# session.headers.update(
#     {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "Accept-Language": "en-US,en;q=0.9",
#     }
# )

# proxy = {
#     "http": "http://brd-customer-hl_a4a3b5b0-zone-youtube_rank:n4n7cvvboqyn@brd.superproxy.io:22225",
#     "https": "http://brd-customer-hl_a4a3b5b0-zone-youtube_rank:n4n7cvvboqyn@brd.superproxy.io:22225",
# }


# def get_info(url):
#     try:
#         response = session.get(f"{url}/questions", proxies=proxy, verify=False)
#         soup = BeautifulSoup(response.text, "html.parser")


#         id_match = re.search(r"(\d+)$", url)
#         university_id = id_match.group(1) if id_match else "Not Found"

#         data = {
#             "University_ID": university_id,
#             "URL": url,
#             "College_Name": "Not Found",
#             "Q/A_Count": "Not Found",
#         }

#         title_tag = soup.find("title")
#         if title_tag:
#             name_match = re.search(r"^(.+?),", title_tag.text)
#             if name_match:
#                 data["College_Name"] = name_match.group(1).strip()

#         meta_description = soup.find("meta", {"name": "Description"})
#         if meta_description:
#             count_match = re.search(
#                 r"See (\d+) Answered Questions", meta_description.get("content", "")
#             )
#             if count_match:
#                 data["Q/A_Count"] = count_match.group(1)

#         return data

#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return None


# info = get_info(
#     "https://www.shiksha.com/college/r-b-mundada-college-of-arts-commerce-and-science-hinjewadi-pune-64929"
# )
# print(info)
