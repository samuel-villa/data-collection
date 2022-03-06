import requests

headers = {
    # 'Connection': 'keep-alive',
    # 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    # 'accept': 'application/json',
    # 'content-type': 'application/x-www-form-urlencoded',
    # 'sec-ch-ua-mobile': '?0',
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    # 'sec-ch-ua-platform': '"Linux"',
    # 'Origin': 'https://openclassrooms.com',
    # 'Sec-Fetch-Site': 'cross-site',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Referer': 'https://openclassrooms.com/',
    # 'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

params = (
    # ('x-algolia-agent', 'Algolia for JavaScript (3.35.1); Browser (lite)'),
    # ('x-algolia-application-id', 'JGRXRFVQM0'),
    # ('x-algolia-api-key', 'cd1e2696005d97e99dc7b882297b09cf'),
)

data = {
  # '{"params":"facets': 'search.category.facetingDisplay"}'
}

response = requests.post('https://jgrxrfvqm0-dsn.algolia.net/1/indexes/PROD_learning-content_EN/query', headers=headers, params=params, data=data)


print(response)