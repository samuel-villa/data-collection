# Data Collection Project
Mix of web scraping programs collecting all kinds of data and exporting datasets.
All programs will store the collected data into a common ```data_storage``` directory structured as follows:
```
data_storage
└── categories
    ├── category_1
    │   ├── website_1
    │   │   ├── YYYYMMDD_hhmmss(1)
    │   │   │   ├── data
    │   │   │   │   └── data.json                             
    │   │   │   └── logfile.log
    │   │   ├── YYYYMMDD_hhmmss(2)
    │   │   └── ...
    │   ├── website_2
    │   └── ...
    ├── category_2
    └── ...
```

___
## Usage
First, install dependencies:
```
$ pip install -r requirements.txt
```
Then, run the program:
```
$ python3 ./main.py
```
___
## Currently Implemented Scrapers

### Udemy Courses
#### https://www.udemy.com/ 
The scraper fetches and collects all courses data present on the Udemy platform. Due to the big amount of 
data available in this website, in addition to get data stored in a single json file, it seemed convenient to also store 
data into multiple json files organized by category.
___
### Pluralsight Courses
#### https://pluralsight.com/
The scraper fetches and collects all courses data present on the Pluralsight platform. Data key values
have been chosen arbitrarily and the data scraping is done by fetching each course url html code.
___
### OpenClassrooms
#### https://openclassrooms.com/
The scraper fetches and collects all courses data present on the Openclassrooms platform. The courses data collected 
includes all free access courses in English and French as well as all Diploma courses in English and French.
___
### GlobalKnowledge
#### https://globalknowledge.com/
The scraper fetches and collects all courses data present on the GlobalKnowledge platform.