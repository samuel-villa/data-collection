# Data Collection Project
Mix of web scraping programs collecting all kind of data and exporting datasets

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
```
python3 ./udemy_courses.py
```
