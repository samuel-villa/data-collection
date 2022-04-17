"""
Collecting the full list of Openclassrooms based courses (free and diploma) in french and english languages.
-> https://openclassrooms.com/en/
-> https://openclassrooms.com/fr/

    * make one POST request in order to get the free courses data in french,
    * make one POST request in order to get the free courses data in english,
    * make one POST request in order to get the diploma courses data in french,
    * make one POST request in order to get the diploma courses data in english,
    * convert data to json format
    * push dictionary into a json file
    * create info log file
"""
import requests
import collector_tools as ct
from datetime import datetime

_CATEGORY = 'education'
_NAME = 'openclassrooms'


def diploma_courses_fr_post_request():
    """
    Collect the french openclassrooms DIPLOMA courses API.
    The data to send in the POST request has been arbitrary modified in order to get all the results in one page and
    avoid looping through the pages (hitsPerPage=1000 instead of 12)
    :return: requests response object
    """
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://openclassrooms.com',
        'Referer': 'https://openclassrooms.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = '{"requests":[{"indexName":"PROD_learning-content_FR","params":"query=&hitsPerPage=1000&maxValuesPerFacet=10&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&facets=%5B%22search.category.facetingDisplay%22%5D&tagFilters=&facetFilters=%5B%22search.type.value%3Apath%22%2C%22search.language.value%3Afr%22%5D"}]}'

    return requests.post(
        'https://jgrxrfvqm0-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(5.7.0)%3B%20JS%20Helper%20(2.28.1)&x-algolia-application-id=JGRXRFVQM0&x-algolia-api-key=cd1e2696005d97e99dc7b882297b09cf',
        headers=headers, data=data)


def diploma_courses_en_post_request():
    """
    Collect the english openclassrooms DIPLOMA courses API.
    The data to send in the POST request has been arbitrary modified in order to get all the results in one page and
    avoid looping through the pages (hitsPerPage=1000 instead of 12)
    :return: requests response object
    """
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://openclassrooms.com',
        'Referer': 'https://openclassrooms.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = '{"requests":[{"indexName":"PROD_learning-content_EN","params":"query=&hitsPerPage=1000&maxValuesPerFacet=10&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&facets=%5B%22search.category.facetingDisplay%22%5D&tagFilters=&facetFilters=%5B%22search.type.value%3Apath%22%2C%22search.language.value%3Aen%22%5D"}]}'

    return requests.post(
        'https://jgrxrfvqm0-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(5.7.0)%3B%20JS%20Helper%20(2.28.1)&x-algolia-application-id=JGRXRFVQM0&x-algolia-api-key=cd1e2696005d97e99dc7b882297b09cf',
        headers=headers, data=data)


def free_courses_fr_post_request():
    """
    Collect the french openclassrooms FREE courses API.
    The data to be sent in the POST request has been arbitrary modified in order to get all the results in one page and
    avoid looping through the pages (hitsPerPage=1000 instead of 10)
    :return: requests response object
    """
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://openclassrooms.com',
        'Referer': 'https://openclassrooms.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = '{"requests":[{"indexName":"PROD_learning-content_FR","params":"query=&hitsPerPage=1000&maxValuesPerFacet=16&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&facets=%5B%22search.language.value%22%2C%22search.type.value%22%2C%22search.category.label%22%5D&tagFilters=&facetFilters=%5B%5B%22search.type.value%3Acourse%22%5D%2C%5B%22search.language.value%3Afr%22%5D%5D"},{"indexName":"PROD_learning-content_FR","params":"query=&hitsPerPage=1&maxValuesPerFacet=16&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=search.type.value&facetFilters=%5B%5B%22search.language.value%3Afr%22%5D%5D"},{"indexName":"PROD_learning-content_FR","params":"query=&hitsPerPage=1&maxValuesPerFacet=16&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=search.language.value&facetFilters=%5B%5B%22search.type.value%3Acourse%22%5D%5D"}]}'

    return requests.post(
        'https://jgrxrfvqm0-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)&x-algolia-application-id=JGRXRFVQM0&x-algolia-api-key=cd1e2696005d97e99dc7b882297b09cf',
        headers=headers, data=data)


def free_courses_en_post_request():
    """
    Collect the english openclassrooms FREE courses API.
    The data to be sent in the POST request has been arbitrary modified in order to get all the results in one page and
    avoid looping through the pages (hitsPerPage=1000 instead of 10)
    :return: requests response object
    """
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://openclassrooms.com',
        'Referer': 'https://openclassrooms.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = '{"requests":[{"indexName":"PROD_learning-content_EN","params":"query=&hitsPerPage=1000&maxValuesPerFacet=16&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&facets=%5B%22search.language.value%22%2C%22search.type.value%22%2C%22search.category.label%22%5D&tagFilters=&facetFilters=%5B%5B%22search.type.value%3Acourse%22%5D%2C%5B%22search.language.value%3Aen%22%5D%5D"},{"indexName":"PROD_learning-content_EN","params":"query=&hitsPerPage=1&maxValuesPerFacet=16&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=search.type.value&facetFilters=%5B%5B%22search.language.value%3Aen%22%5D%5D"},{"indexName":"PROD_learning-content_EN","params":"query=&hitsPerPage=1&maxValuesPerFacet=16&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=search.language.value&facetFilters=%5B%5B%22search.type.value%3Acourse%22%5D%5D"}]}'

    return requests.post(
        'https://jgrxrfvqm0-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)&x-algolia-application-id=JGRXRFVQM0&x-algolia-api-key=cd1e2696005d97e99dc7b882297b09cf',
        headers=headers, data=data)


def get_courses_api(post_response):
    """
    Convert the response from the POST request to json and locate the list of courses with their data
    :param post_response: request response object
    :return: [dict] courses data in json format
    """
    return post_response.json()['results'][0]['hits']


def main():
    """
    Push data collected into one unique json file
    Create log file
    """
    global_work_start_time = datetime.now()
    files = ct.init_data_storage_dir(_CATEGORY, _NAME)

    # get data
    free_fr_courses_data = get_courses_api(free_courses_fr_post_request())
    free_en_courses_data = get_courses_api(free_courses_en_post_request())
    diploma_fr_courses_data = get_courses_api(diploma_courses_fr_post_request())
    diploma_en_courses_data = get_courses_api(diploma_courses_en_post_request())

    # count courses
    free_fr_courses_data_count = len(free_fr_courses_data)
    free_en_courses_data_count = len(free_en_courses_data)
    diploma_fr_courses_data_count = len(diploma_fr_courses_data)
    diploma_en_courses_data_count = len(diploma_en_courses_data)
    courses_count = sum([free_fr_courses_data_count, free_en_courses_data_count, diploma_fr_courses_data_count, diploma_en_courses_data_count])

    # push courses data to file
    ct.push_data2json(files['json_filename'], free_fr_courses_data, _NAME)
    ct.push_data2json(files['json_filename'], free_en_courses_data, _NAME)
    ct.push_data2json(files['json_filename'], diploma_fr_courses_data, _NAME)
    ct.push_data2json(files['json_filename'], diploma_en_courses_data, _NAME)

    # calculate working time
    global_work_end_time = datetime.now()
    global_work_duration = global_work_end_time - global_work_start_time

    # logs
    log_date = f"Date                    : {global_work_start_time}\n"
    log_courses_counter = f"Total courses           : {courses_count}\n"
    log_free_fr_courses_data_count = f"  - free courses (FR)   : {free_fr_courses_data_count}\n"
    log_free_en_courses_data_count = f"  - free courses (EN)   : {free_en_courses_data_count}\n"
    log_diploma_fr_courses_data_count = f"  - diploma courses (FR): {diploma_fr_courses_data_count}\n"
    log_diploma_en_courses_data_count = f"  - diploma courses (EN): {diploma_en_courses_data_count}\n"
    log_total_work_time = f"Total work time         : {global_work_duration}\n"
    log_data_size = f"Data size               : {ct.get_dir_size(files['data_path'])}\n\n"
    ct.write_log(files['log_filename'], log_date)
    ct.write_log(files['log_filename'], log_courses_counter)
    ct.write_log(files['log_filename'], log_free_fr_courses_data_count)
    ct.write_log(files['log_filename'], log_free_en_courses_data_count)
    ct.write_log(files['log_filename'], log_diploma_fr_courses_data_count)
    ct.write_log(files['log_filename'], log_diploma_en_courses_data_count)
    ct.write_log(files['log_filename'], log_total_work_time)
    ct.write_log(files['log_filename'], log_data_size)

    print(f"\n==> DONE <==\n\n-> COLLECTED {courses_count} courses in {global_work_duration}")


if __name__ == '__main__':
    main()
    