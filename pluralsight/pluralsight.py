"""
Collecting the full list of PluralSight based courses
-> https://www.pluralsight.com/

    * inspect the PluralSight sitemap and collect all courses links
    * inspect each link page html code and fetch data,
    * store data into dictionary
    * push dictionary into a json file
    * create info log file
    * problematic urls are stored in order to be processed later on
    * once the main scraping is finished, the problematic urls are processed again for a max number of attempts
"""
import collector_tools
from datetime import datetime

_CATEGORY = 'education'
_NAME = 'pluralsight'
SITEMAP_URL = "https://www.pluralsight.com/sitemap.xml"
COURSES_URL = "https://www.pluralsight.com/courses/"
ERROR_URLS_MAX_ATTEMPTS = 3

keys = {
    'prod_id': '',
    'url': '',
    'title': '',
    'thumbnail': '',
    'description': '',
    'authors': '',
    'authors_about': '',
    'authors_url': '',
    'roles': '',
    'skill_levels': '',
    'publish_date': '',
    'rating': '',
    'rating_count': '',
    'duration': '',
    'retired': '',
    'updated_date': '',
}

testing_links = [
    "https://www.pluralsight.com/courses/insights-observations-data-executive-briefing",
    "https://www.pluralsight.com/courses/your-first-day-rotoscoping-nuke-1217",
    "https://www.pluralsight.com/courses/inverted-triangle-css-intro",
    "https://www.pluralsight.com/courses/inverted-triangle-ERROR_TEST",
    # "https://www.pluralsight.com/courses/java-unit-testing-junit",  # redirection
    "https://www.pluralsight.com/courses/querying-converting-ERROR_TEST",
]

data_path = collector_tools.create_storage_dir(_CATEGORY, _NAME)
json_filename = data_path + _NAME + '.json'
log_path = data_path.replace('data/', '')
log_filename = log_path + _NAME + '.log'
collector_tools.init_json_file(json_filename, _NAME)
collector_tools.init_log(log_filename)


def _get_courses_links():
    """
    Parse the Pluralsight sitemap url and collect all courses urls
    :return: [list] courses urls
    """
    sp = collector_tools.get_soup(SITEMAP_URL)
    xml_loc = sp.find_all("loc")
    courses_links = []
    for link in xml_loc:
        if COURSES_URL in str(link):
            courses_links.append(link.text)
    return list(dict.fromkeys(courses_links))  # remove duplicates if any


def _scrape_html(url, dict_keys):
    """
    Scrape PluralSight url in order to get specific values
    :param url: [str] PluralSight url to scrape
    :param dict_keys: [dict] reset dictionary containing all specific keys we want to scrape
    """
    soup = collector_tools.get_soup(url)
    dict_keys = dict_keys.fromkeys(dict_keys)  # reset dict values

    dict_keys["prod_id"] = soup.find("meta", {"name": "prodId"}).get('content') if soup.find("meta", {
        "name": "prodId"}) else None
    dict_keys["url"] = url
    dict_keys["title"] = soup.find(id='course-page-hero').find('h1').text if soup.find(id='course-page-hero') else None
    dict_keys["thumbnail"] = soup.find("meta", {"name": "thumbnail"}).get('content') if soup.find("meta", {
        "name": "thumbnail"}) else None
    dict_keys["description"] = soup.find("meta", {"name": "description"}).get('content') if soup.find("meta", {
        "name": "description"}) else None
    dict_keys["authors"] = soup.find("meta", {"name": "authors"}).get('content') if soup.find("meta", {
        "name": "authors"}) else None
    dict_keys["authors_about"] = soup.find("div", {"class": "author-item"}).find("p").text if soup.find("div", {
        "class": "author-item"}) else None
    dict_keys["authors_url"] = soup.find("div", {"class": "author-item"}).find('a').get('href') if soup.find("div", {
        "class": "author-item"}) else None
    dict_keys["roles"] = soup.find("meta", {"name": "roles"}).get('content') if soup.find("meta",
                                                                                          {"name": "roles"}) else None
    dict_keys["skill_levels"] = soup.find("meta", {"name": "skill-levels"}).get('content') if soup.find("meta", {
        "name": "skill-levels"}) else None
    dict_keys["publish_date"] = soup.find("meta", {"name": "publish-date"}).get('content') if soup.find("meta", {
        "name": "publish-date"}) else None
    dict_keys["rating"] = soup.find("meta", {"name": "rating"}).get('content') if soup.find("meta", {"name": "rating"}) \
        else None
    dict_keys["rating_count"] = soup.find("meta", {"name": "rating-count"}).get('content') if soup.find("meta", {
        "name": "rating-count"}) else None
    dict_keys["duration"] = soup.find("meta", {"name": "duration"}).get('content') if soup.find("meta", {
        "name": "duration"}) else None
    dict_keys["retired"] = soup.find("meta", {"name": "retired"}).get('content') if soup.find("meta", {
        "name": "retired"}) else None
    dict_keys["updated_date"] = soup.find("meta", {"name": "updated-date"}).get('content') if soup.find("meta", {
        "name": "updated-date"}) else None


def main(keys_dict):
    """
    Main PluralSight scraper
    Loops on all courses url, collect and store data in a json file
    :param keys_dict: [dict] keys we want to collect and store
    """
    global_work_start_time = datetime.now()
    courses_lks = _get_courses_links()  # 13147
    courses_counter = 1
    error_links = []
    error_links_counter = 0

    for lk in testing_links:
        print(courses_counter, 'working on: ', lk)
        log = f"{courses_counter} - working on: {lk} ... "
        collector_tools.write_log(log_filename, log)
        try:
            _scrape_html(lk, keys_dict)
            collector_tools.push_data2json(json_filename, keys_dict, _NAME)
            log = "DONE\n"
            collector_tools.write_log(log_filename, log)
        except TypeError:  # if webpage is not loading or the url is not correct a TypeError is raised
            log = "ERROR <==================\n"
            collector_tools.write_log(log_filename, log)
            error_links.append(lk)
            error_links_counter += 1

        courses_counter += 1

    global_work_end_time = datetime.now()
    global_work_duration = global_work_end_time - global_work_start_time
    print(global_work_duration)

    log = "\n====================== TOTAL ======================\n\n"
    log_date = f"Date           : {global_work_start_time}\n"
    log_courses_counter = f"Nb. courses    : {courses_counter - 1}\n"
    log_total_work_time = f"Total work time: {global_work_duration}\n"
    log_data_size = f"Data size      : {collector_tools.get_dir_size(data_path)}\n\n"
    collector_tools.write_log(log_filename, log)
    collector_tools.write_log(log_filename, log_date)
    collector_tools.write_log(log_filename, log_courses_counter)
    collector_tools.write_log(log_filename, log_total_work_time)
    collector_tools.write_log(log_filename, log_data_size)

    log_err = "\n====================== ERRORS ======================\n\n"
    collector_tools.write_log(log_filename, log_err)
    if error_links_counter > 0:
        log_err_msg = f"{error_links_counter} urls didn't load correctly:\n\n"
        collector_tools.write_log(log_filename, log_err_msg)
        err_index = 1
        for link in error_links:
            log_err_link = f"{err_index}\t{link}\n"
            collector_tools.write_log(log_filename, log_err_link)
            err_index += 1
    else:
        log_err_msg = f"No errors"
        collector_tools.write_log(log_filename, log_err_msg)

    attempt = 0
    log_ricover = "\n====================== RICOVER URLS ======================\n\n"
    collector_tools.write_log(log_filename, log_ricover)
    while attempt < ERROR_URLS_MAX_ATTEMPTS:
        for url in error_links:
            log = f"attempt {attempt + 1} - working on: {url} ... "
            collector_tools.write_log(log_filename, log)
            try:
                _scrape_html(url, keys_dict)
                collector_tools.push_data2json(json_filename, keys_dict, _NAME)
                log = f"{url} RICOVERED\n"
                collector_tools.write_log(log_filename, log)
                error_links.remove(url)
            except TypeError:
                log = "ERROR <==================\n"
                collector_tools.write_log(log_filename, log)
        attempt += 1


if __name__ == '__main__':
    main(keys)
