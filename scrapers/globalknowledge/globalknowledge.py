"""
Collecting the full list of GlobalKnowledge based courses.
-> https://www.globalknowledge.com

    * make one GET request in order to get all courses of a specific topic,
    * loop through all topics and append courses into a list
    * remove all duplicates
    * push collected data into a json file
    * create info log file
"""
import requests
from datetime import datetime
from utils import collector_tools as ct, constants as c

_CATEGORY = c.CATEGORIES['education']
_NAME = 'globalknowledge'

MAX_TOPIC_ID = 101  # max 101


def get_courses(topic_id):
    """
    Send GET request to get all courses of a specific topic.
    In 'params.PageSize' the value has been arbitrary set to 500 in order to get all courses in one page. After a few
    tests it seems that for each topic the number of courses don't pass 200.
    :param topic_id: [int] topic id
    :return: requests response object containing all topic courses
    """
    cookies = {
        'ASP.NET_SessionId': '0zclyskzb3ijd5vxncujjsyp',
        'ApplicationGatewayAffinity': 'd0359f9f8876c542719ed0912d92bd9ceb0f65ab8e87926ae901fb8db6cc4ce0',
        'ApplicationGatewayAffinityCORS': 'd0359f9f8876c542719ed0912d92bd9ceb0f65ab8e87926ae901fb8db6cc4ce0',
        'SC_ANALYTICS_GLOBAL_COOKIE': '4e590c46dddc4bb38d195616098ffdcb|True',
        '__zlcmid': '19XkrJSInZgrNmk',
        'globalknowledge.com#lang': 'en',
        'gk_preferences': 'accepted',
        'gk_performance': 'accepted',
        'gk_cookieControl': 'accepted',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://www.globalknowledge.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'PageSize': '500',
        'PageNo': '1',
        'TechTypes': topic_id,
        'SortDirection': 'ASC',
        'OrderBy': 'Name',
    }

    return requests.get('https://www.globalknowledge.com/en/baps/Search/SearchCourseCatalogueJSON', headers=headers,
                        params=params, cookies=cookies)


def run():
    """
    Main GlobalKnowledge scraper
    """
    global_work_start_time = datetime.now()
    files = ct.init_data_storage_dir(_CATEGORY, _NAME)

    # get data from API
    courses_data = []
    courses_categories = 0
    topic = 1
    courses_counter = 0
    while topic <= MAX_TOPIC_ID:
        nb_categ_courses = get_courses(topic).json()['TotalResults']
        if nb_categ_courses:
            print(f"-> collecting courses from category '{courses_categories + 1}' - {nb_categ_courses} courses")
            courses = get_courses(topic).json()['Results']
            courses_counter += nb_categ_courses
            for course in courses:
                courses_data.append(course)
        else:
            print(f"---> NO COURSES in category '{courses_categories + 1}' <--- ")
        courses_categories += 1
        topic += 1
    print(f"\n{courses_counter} courses collected")

    # remove duplicates (one course can belong to more than one category)
    unique_courses_data = {each['Code']: each for each in courses_data}.values()
    print(f"{len(unique_courses_data)} courses left after removing duplicates")

    # push courses data to file
    for c in unique_courses_data:
        ct.push_data2json(files['json_filename'], c, _NAME)

    # calculate working time
    global_work_end_time = datetime.now()
    global_work_duration = global_work_end_time - global_work_start_time

    # logs
    log_date = f"Date                    : {global_work_start_time}\n"
    log_courses_counter = f"Total courses           : {len(unique_courses_data)}\n"
    log_courses_categories = f"Total courses categories: {courses_categories}\n"
    log_total_work_time = f"Total work time         : {global_work_duration}\n"
    log_data_size = f"Data size               : {ct.get_dir_size(files['data_path'])}\n\n"
    ct.write_log(files['log_filename'], log_date)
    ct.write_log(files['log_filename'], log_courses_counter)
    ct.write_log(files['log_filename'], log_courses_categories)
    ct.write_log(files['log_filename'], log_total_work_time)
    ct.write_log(files['log_filename'], log_data_size)

    print(f"\n==> DONE <==\n\n-> COLLECTED {len(unique_courses_data)} courses in {global_work_duration}")


if __name__ == '__main__':
    run()
