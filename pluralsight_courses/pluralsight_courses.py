"""
For now the best solution is probably to parse all links and get data from html code
values to get:
    * prod_id
    * title
    * url
    * thumbnail
    * authors
    * authors_about
    * authors_url
    * roles
    * skill-levels
    * publish-date
    * rating
    * rating-count
    * duration
    * summary
    * updated date

TODO init json file to store data
"""
import requests
import json
from bs4 import BeautifulSoup

# sitemap_url = "https://www.pluralsight.com/sitemap.xml"
# courses_root_url = "https://www.pluralsight.com/courses/"
# r = requests.get(sitemap_url)
# soup = BeautifulSoup(r.text, "lxml")
# xml_loc = soup.find_all("loc")
# courses_links = []

# for link in xml_loc:
#     if courses_root_url in str(link):
#         courses_links.append(link)
#         print(link.text)

# print(len(xml_loc))
# print(len(courses_links))  # no duplicates

testing_links = [
    "https://www.pluralsight.com/courses/code-first-entity-framework-legacy-databases",
    "https://www.pluralsight.com/courses/querying-converting-data-types-r",
    "https://www.pluralsight.com/courses/building-features-image-data"
]

for lk in testing_links:
    r = requests.get(lk)
    soup = BeautifulSoup(r.text, "lxml")
    prod_id = soup.select('head > meta:nth-child(24)')[0].get('content')
    url = lk
    title = soup.find(id='course-page-hero').find('h1').text
    thumbnail = soup.select('head > meta:nth-child(15)')[0].get('content')
    description = soup.select('head > meta:nth-child(8)')[0].get('content')
    authors = soup.select('head > meta:nth-child(16)')[0].get('content')
    authors_about_check = \
        soup.select('#content > div.course-content-main > div > div > div.course-content-container > div '
                    '> div.course-page-section.course-page-last > div > p')
    authors_about = soup.select('#content > div.course-content-main > div > div > div.course-content-container > div '
                                '> div.course-page-section.course-page-last > div > p')[
        0].text if authors_about_check else authors_about_check
    authors_url = soup.select(
        '#content > div.course-content-main > div > div > div.course-content-container > div > '
        'div.course-page-section.course-page-last > div > div.author-profile > a')[
        0].get('href') if authors_about_check else authors_about_check
    roles = soup.select('head > meta:nth-child(17)')[0].get('content')
    skill_levels = soup.select('head > meta:nth-child(20)')[0].get('content')
    publish_date = soup.select('head > meta:nth-child(21)')[0].get('content')
    rating = soup.select('head > meta:nth-child(22)')[0].get('content')
    rating_count = soup.select('head > meta:nth-child(23)')[0].get('content')
    duration = soup.select('#content > div.course-content-main > div > div > div.course-content-container > div > '
                           'aside > div:nth-child(2) > div:nth-child(5) > div:nth-child(2)')[0].text
    summary = soup.select('#content > div.course-content-main > div > div > div.course-content-container > div > '
                          'div:nth-child(3)')[0].text
    updated_date = soup.select('head > meta:nth-child(30)')[0].get('content')
