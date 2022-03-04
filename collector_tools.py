"""
Tools needed to store and order data collected via other modules
TODO loggers
TODO working time calculator
TODO storage weight calculator
"""
import json
import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime


ROOT = "./data_storage/"
ROOT_CATEGORIES = ROOT + "categories"
CATEGORIES_LIST_FILE = "categories_list.txt"


def create_storage_dir(category, name):
    """
    Generates data storage directories tree specific to a collector module
    :param category: [str] module category
    :param name: [str] module collector name
    :return: full directory path
    """
    date_now = datetime.now()
    timestamp = str(date_now).split(".")[0].replace("-", "").replace(" ", "_").replace(":", "")
    data_path = ROOT_CATEGORIES + '/' + category + '/' + name + '/' + timestamp + '/' + 'data/'
    os.makedirs(data_path, exist_ok=True)
    return data_path


def create_global_categories_dir_tree(root, cat_file):
    """
    Fetch the given txt file where all categories used within the project are listed and create all corresponding
    directories if they don't exist.
    :param root: [str] data storage categories directories tree root
    :param cat_file: [str] categories list file
    """
    with open(cat_file) as f:
        for line in f:
            leave = line.strip()
            path = root + '/' + leave
            os.makedirs(path, exist_ok=True)


# create_global_categories_dir_tree(ROOT_CATEGORIES, CATEGORIES_LIST_FILE)
# p = create_storage_dir('education', 'pluralsight_courses')


def init_json_file(json_filename, root_key):
    """
    Create new json file and initialize it with generic empty dictionary
    :param json_filename: [str] JSON file name
    :param root_key: [str] json root key name
    """
    root = {root_key: []}
    json_object = json.dumps(root, indent=4)
    with open(json_filename, "w") as file:
        file.write(json_object)


def push_data2json(filename, data, root_key):
    """
    Append data to existing json file
    :param filename: [str] json file name
    :param data: [dict] data to be appended
    :param root_key: [str] json root key name
    """
    with open(filename, 'r+') as f:
        file_data = json.load(f)  # load existing data
        file_data[root_key].append(data)  # join new_data with file_data already into file
        f.seek(0)  # sets f's current position at offset
        json.dump(file_data, f, indent=4)  # convert back to json


def get_soup(target, parser):
    """
    Parse web page
    :param target: [str] target page url
    :param parser: [str] parser type (html, lxml)
    :return: bs4 object
    """
    response = requests.get(target)
    html = response.text
    return BeautifulSoup(html, parser)
