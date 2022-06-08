CATEGORIES = {
    'education': 'education',
}
CLI_CMDS = {
    'scrapers': {
        'cdm': 'scrapers',
        'opts': ['-d'],
        'args': True,
        'help': 'List all scraping machines or get more accurate result by adding one or more scrapers category names'
                '\n\n[OPTION]... [category]...'
                '\n\n-d -> details'
    },
    'categories': {
        'cdm': 'categories',
        'opts': ['-d'],
        'args': False,
        'help': 'List all scraping machines categories.'
                '\n\n[OPTION]...'
                '\n\n-d -> details'
    },
    'run': {
        'cdm': 'run',
        'opts': [],
        'args': True,
        'help': 'Run scraper.'
                '\n\n[scraper]...'
    },
}