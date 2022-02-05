"""
Collecting the full list of Udemy based courses

    * check if links to fetch start with /topic/...
"""
import requests
from bs4 import BeautifulSoup
import json

headers = {
    'authority': 'www.udemy.com',
}

params = (
    ('page_size', '16'),
    ('subcategory', ''),
    ('instructional_level', ''),
    ('lang', ''),
    ('price', ''),
    ('duration', ''),
    ('closed_captions', ''),
    ('subs_filter_type', ''),
    ('label_id', '7380'),
    ('source_page', 'topic_page'),
    ('locale', 'en_US'),
    ('currency', 'eur'),
    ('navigation_locale', 'en_US'),
    ('skip_price', 'true'),
    ('sos', 'pl'),
    ('fl', 'lbl'),
)

# parsing all 'topic' links into udemy sitemap page
target_sitemap = "https://www.udemy.com/sitemap/"


def get_sitemap_soup(target):
    """
    parse Udemy sitemap page
    :param target: target page url
    :return: bs4 object
    """
    response = requests.get(target)
    html = response.text
    return BeautifulSoup(html, "html.parser")


def get_topic_links(bs4_soup):
    """
    parse Udemy sitemap page and collect all links ('href') containing the word 'topic'
    :param bs4_soup: bs4 object
    :return: list containing all links
    """
    links = []
    for link in bs4_soup.find_all("a"):
        if '/topic/' in link.get("href"):
            links.append(link.get("href"))
    return links


soup = get_sitemap_soup(target_sitemap)
topic_links = get_topic_links(soup)



# categories = soup.find_all("ul")
# print(categories[1])  # index 1-13
#
# for i in categories[1]:
#     print(i)




"""
# get all courses within one category
current_page = 1
total_page = 1  # set to 1 before to enter the loop in order to give it the time to be updated within the loop
category_id = 7380  # python category example

# while current_page <= total_page:
response = requests.get(f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?closed_captions=&currency=eur&duration=&fl=lbl&instructional_level=&label_id={category_id}&lang=&locale=en_US&navigation_locale=en_US&page_size=16&price=&skip_price=true&sos=pl&source_page=topic_page&subcategory=&subs_filter_type=&p={current_page}")
print(response.status_code)
html = response.text
json_file = json.loads(html)
# print(json.dumps(json_file, indent=4))
if total_page == 1:
    total_page = json_file['unit']['pagination']['total_page']
# for i in json_file['unit']['items']:
#     print(i)
# current_page += 1
"""




# # Directly from dictionary
# with open('json_data.json', 'w') as outfile:
#     json.dump(json_string, outfile)
#
# # Using a JSON string
# with open('json_data.json', 'w') as outfile:
#     outfile.write(json_string)