"""
Tools needed to store and order data collected via other modules
"""
import json
import os
import subprocess
from bs4 import BeautifulSoup
import requests
from datetime import datetime


_ROOT = "./data_storage/"
_ROOT_CATEGORIES = _ROOT + "categories"
ROOT = "data_storage/"
ROOT_CATEGORIES = ROOT + "categories"
CATEGORIES_LIST_FILE = "../categories_list.txt"


def get_dir_size(dir_path):
    """
    Calculate the size of the given directory
    :param dir_path: [str] directory path
    :return: [str] directory size
    """
    return subprocess.check_output(['du', '-sh', dir_path]).split()[0].decode('utf-8')


def create_storage_dir(category, name):
    """
    Generates data storage directories tree specific to a collector module.
    This function is called from the specific collector module.
        Ex: 'data_storage/categories/music/piano_courses/20220304_230413/data/'
    :param category: [str] module category
    :param name: [str] module collector name
    :return: full directory path
    """
    date_now = datetime.now()
    timestamp = str(date_now).split(".")[0].replace("-", "").replace(" ", "_").replace(":", "")
    data_path = ROOT_CATEGORIES + '/' + category + '/' + name + '/' + timestamp + '/' + 'data/'
    os.makedirs(data_path, exist_ok=True)
    return data_path


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


def init_log(log_filename):
    """
    Initialize log file
    :param log_filename: [str] log file name
    """
    with open(log_filename, 'a') as f:
        f.write("====================== LOGFILE ======================\n\n")
        
        
def init_data_storage_dir(scraper_category, scraper_name):
    """
    Initialize data storage directory and files
    :param scraper_category: [str] main scraper category name
    :param scraper_name: [str] main scraper name
    :return: [dict] useful paths
        - data_path:     ../data_storage/categories/<category>/<scraper_name>/<timeframe>/data/
        - json_filename: ../data_storage/categories/<category>/<scraper_name>/<timeframe>/data/<scraper_name>.json
        - log_filename:  ../data_storage/categories/<category>/<scraper_name>/<timeframe>/<scraper_name>.log
    """
    data_path = create_storage_dir(scraper_category, scraper_name)
    json_filename = data_path + scraper_name + '.json'
    log_path = data_path.replace('data/', '')
    log_filename = log_path + scraper_name + '.log'
    init_json_file(json_filename, scraper_name)
    init_log(log_filename)
    return {
        'data_path': data_path,
        'json_filename': json_filename,
        'log_filename': log_filename
    }


def init_data_storage_dir_for_categories(scraper_category, scraper_name, categories_dir):
    """
    Initialize data storage directory and files.
    This function is more appropriate 'init_data_storage_dir' for larger amounts of data, where dividing data in
    categories is more convenient.
    :param scraper_category: [str] main scraper category name
    :param scraper_name: [str] main scraper name
    :param categories_dir: [str] directory name where data divided by categories will be stored
    :return: [dict] useful paths
        - data_path:       ../data_storage/categories/<category>/<scraper_name>/<timeframe>/data/
        - categories_path: ../data_storage/categories/<category>/<scraper_name>/<timeframe>/data/<categories_dir>/
        - json_filename:   ../data_storage/categories/<category>/<scraper_name>/<timeframe>/data/<scraper_name>.json
        - log_filename:    ../data_storage/categories/<category>/<scraper_name>/<timeframe>/<scraper_name>.log
    """
    data_path = create_storage_dir(scraper_category, scraper_name)
    json_filename = data_path + scraper_name + '.json'
    log_path = data_path.replace('data/', '')
    log_filename = log_path + scraper_name + '.log'
    init_json_file(json_filename, scraper_name)
    init_log(log_filename)
    categories_path = data_path + categories_dir + '/'
    os.makedirs(categories_path, exist_ok=True)
    return {
        'data_path': data_path,
        'json_filename': json_filename,
        'log_filename': log_filename,
        'categories_path': categories_path
    }


def make_single_json_from_categories(unique_json_filepath, root, category_path):
    """
    Generate one single json file merging all files present in the 'category_path' folder
    :param unique_json_filepath: [str] unique json filepath
    :param root: root key name (scraper name)
    :param category_path: categories json files directory
    """
    init_json_file(unique_json_filepath, root)
    data = {root: []}
    for jsonfile in os.listdir(category_path):
        json_filepath = category_path + jsonfile
        with open(json_filepath, 'r+') as infile:
            data[root].append(json.load(infile))
        with open(unique_json_filepath, 'r+') as outfile:
            json.dump(data, outfile, indent=4)


def write_log(log_filename, log_msg):
    """
    Write into log file
    :param log_filename: [str] log file name
    :param log_msg: [str] log message to append
    """
    with open(log_filename, 'a') as f:
        f.write(log_msg)


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


def get_soup(target):
    """
    Parse web page
    :param target: [str] target page url
    :return: bs4 object
    """
    response = requests.get(target)
    if response.status_code != 200:
        return 'response.status_code: ' + str(response.status_code)
    html = response.text
    return BeautifulSoup(html, "lxml")


def get_endpoints_containing(word, bs4_soup):
    """
    parse Globalknowledge page, collect all links ('href') containing the given 'word' and remove all duplicates
    :param word: [str] part of url that the endpoint must contain
    :param bs4_soup: bs4 object
    :return: [list] unique links
    """
    links = []
    for lk in bs4_soup.find_all("a"):
        if word in str(lk.get("href")):
            links.append(lk.get("href"))
    return list(dict.fromkeys(links))
