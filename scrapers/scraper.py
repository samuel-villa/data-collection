from utils import collector_tools as ct, constants as c


class Scraper:
    """
    Main scraper class from which single scrapers will inherit.
    """
    def __init__(self, name, category):
        self.name = name
        self.category = category
