# Data Collection Project
Mix of web scraping programs collecting all kinds of data and exporting datasets.
All programs (temporarily except 'Udemy') will store the collected data into a common ```data_storage``` directory structured as follows:
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

## Udemy Courses
The aim of this program is to fetch and collect all courses data present on the Udemy platform.

### Data Organization
The data collected is structured as follows:
```
YYYYMMDD_hhmmss
├── YYYYMMDD_hhmmss.log
├── udemy_courses_data
│   ├── 0000_first-category.json
│   ├── 0001_second-category.json
│   └── ...
└── udemy_courses_full_list.json
```
Courses data are organized by category. The folder ```udemy_courses_data``` contains one json file per category.
The main collection folder ```YYYYMMDD_hhmmss``` contains another global json file (```udemy_courses_full_list.json```) grouping all courses still organized by category and a log file (```YYYYMMDD_hhmmss.log```) providing some information about the collection like the number of categories collected, the number of courses collected, the collection worktime, date and time information, etc.

### Usage
First, install dependencies:
```
$ pip install -r requirements.txt
```
Then, run the program:
```
$ python3 ./udemy_courses.py
```
___

## Pluralsight Courses
The aim of this program is to fetch and collect all courses data present on the Pluralsight platform. Data key values
have been chosen arbitrarily and the data scraping is done by fetching each course url html code.

### Usage
First, install dependencies:
```
$ pip install -r requirements.txt
```
Then, run the program:
```
$ python3 ./pluralsight.py
```
___