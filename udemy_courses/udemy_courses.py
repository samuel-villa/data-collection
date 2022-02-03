"""
Collecting the full list of Udemy based courses
"""
from urllib.request import urlopen

url = "https://www.udemy.com/sitemap/"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)
