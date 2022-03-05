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
ROOT = "../data_storage/"
ROOT_CATEGORIES = ROOT + "categories"
CATEGORIES_LIST_FILE = "categories_list.txt"


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
    This function should be called from the specific collector module, that's why the path starts with '../'
        Ex: '../data_storage/categories/music/piano_courses/20220304_230413/data/'
    :param category: [str] module category
    :param name: [str] module collector name
    :return: full directory path
    """
    date_now = datetime.now()
    timestamp = str(date_now).split(".")[0].replace("-", "").replace(" ", "_").replace(":", "")
    data_path = ROOT_CATEGORIES + '/' + category + '/' + name + '/' + timestamp + '/' + 'data/'
    os.makedirs(data_path, exist_ok=True)
    return data_path


def _create_global_categories_dir_tree(root, cat_file):
    """
    FIXME DEPRECATED: create_storage_dir() does the exact same thing without the need to parse an extra txt file listing
        the categories
    Fetch the given txt file where all categories used within the project are listed and create all corresponding
    directories if they don't exist.
    :param root: [str] data storage categories directories tree root
    :param cat_file: [str] categories list file
    """
    with open(cat_file) as f:
        for line in f:
            leave = line.strip()
            print(line)
            path = root + '/' + leave
            os.makedirs(path, exist_ok=True)


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
