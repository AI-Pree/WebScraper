import jobAutoamtion
import webscrapseek
import parsedata
import logging
import logging.config
import json
import os

#load the logging configuration
def setup_logging(default_path = 'logging.json',default_level = logging.INFO):
    #set up configuration
    if os.path.exists(default_path):
        with open(default_path, 'rt') as fs:
            config = json.load(fs)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level =  default_level)

def main():
    setup_logging()
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger(__name__)
    search_url = "https://www.seek.com.au/python-jobs-in-information-communication-technology/full-time?daterange=3&salaryrange=200000-999999&salarytype=annual"
    base_url = "https://www.seek.com.au"
    scraper = webscrapseek.Webscraper(_base_url= base_url, _search_url = search_url)
    scraper.parsePage()
    automate = jobAutoamtion.Automate()
    automate.apply(base_url)


if __name__ == '__main__':
    main()  