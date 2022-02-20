"""
Collecting the full list of Udemy based courses

    * check if links to fetch start with /topic/...
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

SITEMAP_URL = "https://www.udemy.com/sitemap/"
BASE_URL = "https://www.udemy.com"
JSON_FILE = 'udemy_courses.json'


def get_sitemap_soup(target):
    """
    parse Udemy sitemap page
    :param target: target page url
    :return: bs4 object
    """
    response = requests.get(target)
    html = response.text
    return BeautifulSoup(html, "html.parser")


def get_topic_endpoints(bs4_soup):
    """
    parse Udemy sitemap page and collect all links ('href') containing the word 'topic'
    :param bs4_soup: bs4 object
    :return: list containing all links
    """
    links = []
    for lk in bs4_soup.find_all("a"):
        if '/topic/' in lk.get("href"):
            links.append(lk.get("href"))
    return links


def get_topic_id(topic_link):
    """
    parse the topic url in order to fetch the category id
    :param topic_link: category url
    :return: category id
    """
    url = BASE_URL + topic_link
    response = requests.get(url)
    html = response.text
    bs4_soup = BeautifulSoup(html, "html.parser")
    for attribute in bs4_soup.find_all('div'):
        if attribute.has_attr('data-component-props'):
            json_part = json.loads(attribute['data-component-props'])
            return json_part["topic"]["id"]
    return None


def collect_topic_courses(topic_id):
    """
    get all courses items of one given category (topic) and push collected data to json file
    :param topic_id: courses category id
    """
    current_page = 1
    total_page = 1  # set to 1 before to enter the loop in order to give it the time to be updated within the loop
    while current_page <= total_page:
        response = requests.get(f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?closed_captions=&currency"
                                f"=eur&duration=&fl=lbl&instructional_level=&label_id={topic_id}&lang=&locale=en_US"
                                f"&navigation_locale=en_US&page_size=60&price=&skip_price=true&sos=pl&source_page"
                                f"=topic_page&subcategory=&subs_filter_type=&p={current_page}")
        if response.status_code == 200:
            html = response.text
            json_data = json.loads(html)
            if total_page == 1:  # update total number of pages
                total_page = json_data['unit']['pagination']['total_page']
            for i in json_data['unit']['items']:
                if i["id"] not in courses_ids:  # check for duplicate courses
                    courses_ids.append(i["id"])  # only needed to count data
                    push_data2json(JSON_FILE, i)
        else:
            print("NO DATA collected for topic ID " + str(topic_id) + " at page: " + str(current_page) +
                  " --> RESP CODE: " + str(response.status_code) + "\n\n==========================================\n\n")
            with open("pages_error.log", 'a') as f:
                f.write("===== NO DATA COLLECTED =====\n\n")
                f.write(f"topic ID     : {topic_id}\n")
                f.write(f"page         : {current_page}\n")
                f.write(f"response code: {response.status_code}\n")
                f.write("=============================\n\n")
        current_page += 1


def init_json_file(json_filename):
    """
    create new json file and initialize it with generic empty dictionary
    """
    root = {"udemy_courses": []}
    json_object = json.dumps(root, indent=4)
    with open(json_filename, "w") as f:
        f.write(json_object)


def push_data2json(filename, data):
    """
    append data to existing json file
    :param filename: json file name
    :param data: data to be appended
    """
    with open(filename, 'r+') as f:
        file_data = json.load(f)  # load existing data
        file_data["udemy_courses"].append(data)  # join new_data with file_data inside udemy_courses
        f.seek(0)  # sets f's current position at offset
        json.dump(file_data, f, indent=4)  # convert back to json


# main
work_start_time = datetime.now()
soup = get_sitemap_soup(SITEMAP_URL)
topic_endpoints = get_topic_endpoints(soup)  # len=341
topic_endpoints_no_duplicates = list(dict.fromkeys(topic_endpoints))  # removing duplicates (len=276)
topic_ids = []
for link in topic_endpoints_no_duplicates:  # CHANGE HERE FOR TESTING (topic_endpoints_no_duplicates[:1])
    topic_ids.append(get_topic_id(link))

init_json_file(JSON_FILE)

courses_ids = []
for topic in topic_ids:
    collect_topic_courses(topic)

work_end_time = datetime.now()
work_duration = work_end_time - work_start_time

with open("data.log", 'w') as f:
    f.write("===== Logfile =====\n\n")
    f.write(f"courses collected: {len(courses_ids)}\n")
    f.write(f"total work time  : {work_duration}\n\n")

print("\n\n---> Dataset created <---")
