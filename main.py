"""
TODO -> CLI < https://dbader.org/blog/how-to-make-command-line-commands-with-python >
    data_collect scrapers            -> list all scrapers
    data_collect scrapers <category> -> list all scrapers of one category
    data_collect categories          -> list all scraper categories
    data_collect logs                -> list all scrapers most recent log file (with creation date)
    data_collect log <name>          -> cat log file
    data_collect run <scraper>       -> start selected scraper process
"""
from scrapers.openclassrooms import openclassrooms
from scrapers.globalknowledge import globalknowledge
from scrapers.pluralsight import pluralsight
from scrapers.udemy import udemy

# udemy.run()
# pluralsight.run()
# globalknowledge.run()
openclassrooms.run()
