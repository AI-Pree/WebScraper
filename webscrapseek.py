#! python3
# webscrapseek.py - webscaper for listing all the jobs that meets the user criteria

from bs4 import BeautifulSoup
import requests
import json
import sys


class Webscraper():
    def __init__(self, _base_url, _search_url):
        self._dataArr = []
        self._base_url = _base_url
        self._search_url = _search_url

    # get the data for the jobs
    def get_job_lists(self, jobs):
        for job in jobs.find_all('article'):
            # only shows up normal jobs
            # chane the condition to premoum job for different search query
            if 'normalJob' in job.attrs['data-automation']:

                title = job.find('a', {'data-automation':'jobTitle'})
                company = job.find('a', {'data-automation':'jobCompany'})
                area = job.find('a', {'data-automation':'jobArea'})
                location = job.find('a', {'data-automation':'jobLocation'})
                job_url = job.find('a', {'data-automation':'jobTitle'})['href']

                # storing the value in data object
                jobDict = {
                    'Title': title.text if title else '',
                    'Company': company.text if company else '',
                    'Area': area.text if area else '',
                    'Location': location.text if location else '',
                    'jobURL': job_url,
                }
                # passing the dict in array
                self._dataArr.append(jobDict)

    # parse the search results
    def parsePage(self):
        # getting HTTP requests
        response = requests.get(self._search_url)
        if response.status_code == requests.codes.ok: #check if the response is received
            # Fetiching html using beautiful soup
            html_doc = BeautifulSoup(response.content, 'html.parser')

            self.get_job_lists(html_doc) #function that stores the job list of current page in dictionaries

            next_page_text = html_doc.find('a', class_ = 'bHpQ-bp')
            if next_page_text:
                partial_page_url = html_doc.find('a', class_ = 'bHpQ-bp')['href']
                next_page_url = self._base_url + partial_page_url
                parsePage(next_page_url)
            
            else:
                # dumping the array in the json file after all the data in the pages are parsed
                with open('seekdata.json', 'w') as output:  
                    json.dump(self._dataArr, output, indent = 4, sort_keys = False)

