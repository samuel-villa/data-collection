"""
Collecting the full list of Udemy based courses
"""
import requests
from bs4 import BeautifulSoup

target_url = "https://www.udemy.com/sitemap/"
headers = {}
params = ()


def html_parser(url, h=None, p=None):
    """
    creating the connection with the target website
    :param url: target url
    :param h: headers
    :param p: parameters
    :return: BeautifulSoup object
    """
    response = requests.get(url, headers=h, params=p)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


print(type(html_parser(target_url)))

