"""
Collecting the full list of Openclassrooms based courses (free and diploma)
-> https://openclassrooms.com/en/

    * make one POST request in order to get the free courses data,
    * make one POST request in order to get the diploma courses data,
    * convert data to json format
    * push dictionary into a json file
    * create info log file  # TODO
"""
import requests
import collector_tools

_CATEGORY = 'education'
_NAME = 'openclassrooms'

data_path = collector_tools.create_storage_dir(_CATEGORY, _NAME)
json_filename = data_path + _NAME + '.json'
log_path = data_path.replace('data/', '')
log_filename = log_path + _NAME + '.log'
collector_tools.init_json_file(json_filename, _NAME)
collector_tools.init_log(log_filename)


def diploma_courses_post_request():
    """
    Collect the openclassrooms DIPLOMA courses API.
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


def free_courses_post_request():
    """
    Collect the openclassrooms FREE courses API.
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


def get_courses_api(post_response):
    """
    Convert the response from the POST request to json and locate the list of courses with their data
    :param post_response: request response object
    :return: [dict] all courses data in json format
    """
    return post_response.json()['results'][0]['hits']


def main():
    """
    Push data collected into one unique json file
    """
    free_courses_data = get_courses_api(free_courses_post_request())  # 416
    diploma_courses_data = get_courses_api(diploma_courses_post_request())  # 35

    collector_tools.push_data2json(json_filename, free_courses_data[:2], _NAME)  # TODO => TESTING
    collector_tools.push_data2json(json_filename, diploma_courses_data[:2], _NAME)  # TODO => TESTING


if __name__ == '__main__':
    main()
