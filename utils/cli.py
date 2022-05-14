"""
TODO -> CLI < https://dbader.org/blog/how-to-make-command-line-commands-with-python >
    < COMMANDS >
    dccli scrapers            -> list all scrapers in table format:
    dccli scrapers <category> -> list all scrapers of one category
 -> name | category | last time used | last time work time | lt records collected | last data collected weight
    --------------------------------------------------------------------
    dccli categories          -> list all scraper categories
 -> category name | nb. scrapers | last time used | last time work time | total records collected | total data collected weight
    --------------------------------------------------------------------
    dccli run <scraper>       -> start selected scraper process
"""
import sys
import os
from . import constants as c, collector_tools as ct


def server():
    # TODO
    """
    Verify commands entered by the user and select the correct function to launch
    :return:
    """
    cmd = c.CLI_CMDS
    if sys.argv[1] == 'hola':
        print("ok")
        print(cmd)
    else:
        print('wrong arg')


def scrapers():
    scrapers_path = "./scrapers/"
    scrapers_list = os.listdir(scrapers_path)
    for scraper in scrapers_list:
        print(scraper)
    print(f"\n{len(scrapers_list)} scrapers found")
