"""
Collecting the full list of Udemy based courses

    * inspect the Udemy sitemap in order to get all categories endpoints (ex. '/web-development/')
    * for each category link:
        - inspect the page in order to get the category ID,
        - insert the category ID in a http request in order to inspect and collect all courses,
        - push all collected courses data into a json file,
    * push all collected categories into a global json file
    * create info log file

TODO make data be stored in the common 'data_storage' folder
"""

import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

_CATEGORY = 'education'
_NAME = 'udemy'
SITEMAP_URL = "https://www.udemy.com/sitemap/"
BASE_URL = "https://www.udemy.com"
DATA_DIR = "./data/"
UDEMY_COURSES_DIR_NAME = "udemy_courses_data/"
MERGED_COURSES_FILENAME = "udemy_courses_full_list"
GLOBAL_ROOT_KEY = "courses_by_topic"

# build directories tree
date_now = datetime.now()  # 2022-02-22 22:22:02.228866
timestamp = str(date_now).split(".")[0].replace("-", "").replace(" ", "_").replace(":", "")  # 20220222_222202
root_path = DATA_DIR + timestamp + "/"  # data/20220222_222202/
udemy_courses_path = root_path + UDEMY_COURSES_DIR_NAME
log_filename = root_path + timestamp + ".log"
merged_courses_file_path = root_path + MERGED_COURSES_FILENAME + ".json"
zip_file_name = root_path + timestamp

# create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(udemy_courses_path, exist_ok=True)


def get_sitemap_soup(target):
    """
    parse Udemy sitemap page
    :param target: target page url
    :return: bs4 object
    """
    response = requests.get(target)
    html = response.text
    return BeautifulSoup(html, "lxml")


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


def collect_topic_courses(cat_id, json_fn, category_name):
    """
    get all courses items of one given category (topic) and push collected data to json file
    :param category_name: category name
    :param json_fn: json filename
    :param cat_id: courses category id
    :return: number of courses collected
    """
    current_page = 1
    total_page = 1  # set to 1 before to enter the loop in order to give it the time to be updated within the loop
    courses_cnt = 0
    courses_ids = []
    while current_page <= total_page:
        response = requests.get(f"https://www.udemy.com/api-2.0/discovery-units/all_courses/?closed_captions=&currency"
                                f"=eur&duration=&fl=lbl&instructional_level=&label_id={cat_id}&lang=&locale=en_US"
                                f"&navigation_locale=en_US&page_size=60&price=&skip_price=true&sos=pl&source_page"
                                f"=topic_page&subcategory=&subs_filter_type=&p={current_page}")
        if response.status_code == 200:
            html = response.text
            json_data = json.loads(html)
            if total_page == 1:  # get total n° of pages from url and update value initially set to '1'
                total_page = json_data['unit']['pagination']['total_page']
            for i in json_data['unit']['items']:
                if i["id"] not in courses_ids:  # check for duplicate courses
                    courses_ids.append(i["id"])
                    push_data2json(json_fn, i, category_name)
                    courses_cnt += 1
        else:
            print("NO DATA collected for topic ID " + str(cat_id) + " at page: " + str(current_page) +
                  " --> RESP CODE: " + str(response.status_code) + "\n\n==========================================\n\n")
            with open("pages_error.log", 'a') as f:
                f.write("===== NO DATA COLLECTED =====\n\n")
                f.write(f"topic ID     : {cat_id}\n")
                f.write(f"page         : {current_page}\n")
                f.write(f"response code: {response.status_code}\n")
                f.write("=============================\n\n")
        current_page += 1
    return courses_cnt


def init_json_file(json_filename, root_key):
    """
    create new json file and initialize it with generic empty dictionary
    :param json_filename: JSON file name
    :param root_key: json root key name
    """
    root = {root_key: []}
    json_object = json.dumps(root, indent=4)
    with open(json_filename, "w") as file:
        file.write(json_object)


def push_data2json(filename, data, root_key):
    """
    append data to existing json file
    :param filename: json file name
    :param data: data to be appended
    :param root_key: category name
    """
    with open(filename, 'r+') as f:
        file_data = json.load(f)  # load existing data
        file_data[root_key].append(data)  # join new_data with file_data inside udemy
        f.seek(0)  # sets f's current position at offset
        json.dump(file_data, f, indent=4)  # convert back to json


def merge_categories2json(new_file, root, cat_dir):
    """
    Merge all categories json files into one json file
    :param new_file: global filename
    :param root: root key name (bypassed, useless)
    :param cat_dir: categories json files directory
    """
    init_json_file(new_file, root)
    data = {root: []}
    for jsonfile in os.listdir(cat_dir):
        json_filepath = cat_dir + jsonfile
        with open(json_filepath, 'r+') as infile:
            data[root].append(json.load(infile))
        with open(new_file, 'r+') as outfile:
            json.dump(data, outfile, indent=4)


def main():
    """
    loop through all categories and collect all courses data
    creates a log file
    """
    global_work_start_time = datetime.now()

    soup = get_sitemap_soup(SITEMAP_URL)
    topic_endpoints = get_topic_endpoints(soup)  # len=341
    unique_topic_endpoints = list(dict.fromkeys(topic_endpoints))  # removing duplicates (len=276)

    total_categories = 0
    total_courses = 0

    print("============================================================")

    for link in unique_topic_endpoints[12:14]:  # CHANGE HERE FOR TESTING (unique_topic_endpoints[12:14])

        topic_id = get_topic_id(link)  # 8322
        topic_name = str(link).split("/")[2]  # "web-development"
        data_filename = udemy_courses_path + str(topic_id) + "_" + str(topic_name) + ".json"
        # data/20220222_222202/udemy_courses_data/8322_web-development.json

        init_json_file(data_filename, topic_name)
        print(f"CATEGORY: {topic_name}")
        print(f"file '{data_filename}' initialized")
        work_start_time = datetime.now()
        courses_count = collect_topic_courses(topic_id, data_filename, topic_name)
        work_end_time = datetime.now()
        work_duration = work_end_time - work_start_time
        print(f"{courses_count} courses collected in {work_duration}")
        print("============================================================\n")

        with open(log_filename, 'a') as f:
            f.write(f"CATEGORY: {topic_name}\n")
            f.write(f"{courses_count} courses collected in {work_duration}\n\n")

        total_categories += 1
        total_courses += courses_count

    global_work_end_time = datetime.now()
    global_work_duration = global_work_end_time - global_work_start_time

    # merging categories into one global file + calculate work time
    merging_start_time = datetime.now()
    merge_categories2json(merged_courses_file_path, GLOBAL_ROOT_KEY, udemy_courses_path)
    merging_end_time = datetime.now()
    merging_duration = merging_end_time - merging_start_time

    with open(log_filename, 'a') as f:
        f.write("====================== TOTAL ======================\n\n")
        f.write(f"Date           : {global_work_start_time}\n")
        f.write(f"Nb. categories : {total_categories}\n")
        f.write(f"Nb. courses    : {total_courses}\n")
        f.write(f"Total work time: {global_work_duration}\n\n")
        f.write(f"Merge work time: {merging_duration}\n")

    print("*** Dataset created ***")


if __name__ == '__main__':
    main()
