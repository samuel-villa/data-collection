"""For now the best solution is probably to parse all links and get data from html code values to get: 'prod_id',
'url', 'title', 'thumbnail', 'description', 'authors', 'authors_about', 'authors_url', 'roles', 'skill_levels',
'publish_date', 'rating', 'rating_count', 'duration', 'retired', 'updated_date'.


"""
import collector_tools

_CATEGORY = 'education'
_NAME = 'pluralsight_courses'
SITEMAP_URL = "https://www.pluralsight.com/sitemap.xml"
COURSES_URL = "https://www.pluralsight.com/courses/"

data_path = collector_tools.create_storage_dir(_CATEGORY, _NAME)
js_filename = data_path + _NAME + '.json'
collector_tools.init_json_file(js_filename, _NAME)


def _get_courses_links():
    """
    Parse the Pluralsight sitemap url and collect all courses urls
    :return: [list] courses urls
    """
    sp = collector_tools.get_soup(SITEMAP_URL, "lxml")
    xml_loc = sp.find_all("loc")
    courses_links = []
    for link in xml_loc:
        if COURSES_URL in str(link):
            courses_links.append(link.text)
    return list(dict.fromkeys(courses_links))  # remove duplicates if there are


# testing_links = [
#     "https://www.pluralsight.com/courses/code-first-entity-framework-legacy-databases",
#     "https://www.pluralsight.com/courses/querying-converting-data-types-r",
#     "https://www.pluralsight.com/courses/building-features-image-data"
# ]


def main():
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

    courses_lks = _get_courses_links()  # 13147
    courses_counter = 1

    for lk in courses_lks:
        print(courses_counter, 'working on: ', lk)
        soup = collector_tools.get_soup(lk, "lxml")

        keys = keys.fromkeys(keys)  # reset dict values

        keys["prod_id"] = soup.find("meta", {"name": "prodId"}).get('content')
        keys["url"] = lk
        keys["title"] = soup.find(id='course-page-hero').find('h1').text
        keys["thumbnail"] = soup.find("meta", {"name": "thumbnail"}).get('content')
        keys["description"] = soup.find("meta", {"name": "description"}).get('content')
        keys["authors"] = soup.find("meta", {"name": "authors"}).get('content')
        is_authors_about = soup.find("div", {"class": "author-item"})
        keys["authors_about"] = is_authors_about.find("p").text if is_authors_about else is_authors_about
        keys["authors_url"] = is_authors_about.find('a').get('href') if is_authors_about else is_authors_about
        keys["roles"] = soup.find("meta", {"name": "roles"}).get('content')
        keys["skill_levels"] = soup.find("meta", {"name": "skill-levels"}).get('content')
        keys["publish_date"] = soup.find("meta", {"name": "publish-date"}).get('content')
        is_rating = soup.find("meta", {"name": "rating"})
        keys["rating"] = is_rating.get('content') if is_rating else is_rating
        is_rating_count = soup.find("meta", {"name": "rating-count"})
        keys["rating_count"] = is_rating_count.get('content') if is_rating_count else is_rating_count
        keys["duration"] = soup.find("meta", {"name": "duration"}).get('content')
        keys["retired"] = soup.find("meta", {"name": "retired"}).get('content')
        keys["updated_date"] = soup.find("meta", {"name": "updated-date"}).get('content')

        collector_tools.push_data2json(js_filename, keys, _NAME)

        courses_counter += 1


if __name__ == '__main__':
    main()
