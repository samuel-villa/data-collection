"""
For now the best solution is probably to parse all links and get data from html code
"""
import requests
import json
from bs4 import BeautifulSoup

courses_root_url = "https://www.pluralsight.com/courses/"
url = "https://www.pluralsight.com/sitemap.xml"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
all_links = soup.find_all("loc")
courses_links = []

for link in all_links:
    if courses_root_url in str(link):
        courses_links.append(link)
        print(link.text)

print(len(all_links))
print(len(courses_links))  # no duplicates
