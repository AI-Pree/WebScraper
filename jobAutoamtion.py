#! python3
# Automation for applying jobs

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import parsedata
from bs4 import BeautifulSoup
import logging
import os


# creating class to make it reusable
class Automate():
    def __init__(self):
        chrome_opt = Options()
        chrome_opt.add_argument('--headless')
        self.driver = Chrome(options = chrome_opt)
        self.logger = logging.getLogger(__name__)
        self.datas = parsedata.ParseJson('seekdata.json')

        
    #loggin in to the site
    def login(self):
        self.logger.info("Opened the site successfully")
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[title = 'Sign in']"))) # waiting for sign in to be loaded
        self.driver.find_element_by_link_text("Sign in").click()
        WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.TAG_NAME, "form"))) # waiting for the form to be loaded 
        self.logger.info("signing in....")
        # can add config file for logging in infos
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "email")))
        #email address to log in
        self.driver.find_element_by_id("email").send_keys("email@gmail.com") 
        #password to log in
        self.driver.find_element_by_id("password").send_keys("password")
        self.driver.find_element_by_xpath("//button[@type = 'submit']").click()
        self.logger.info("logged in successfully")
        self.logger.info("working!!")

    def applyJob(self):           
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT,"Apply")))
        self.driver.find_element_by_link_text('Apply').click()
        delay = 2#waiting time for the element to load
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, "fieldset"))) # waits for 3secs to check if the element fieldset is loaded     
        except TimeoutException:
            self.logger.exception("Extended amount time error")
        finally:
            self.driver.find_element_by_id("uploadresume").click()

            if  os.path.exists(os.getcwd()+"/resume.txt"):
                self.driver.find_element_by_xpath("//input[@id='resumeFile'][@type = 'file']").send_keys(os.getcwd()+"/resume.text")
            else:
                self.driver.find_element_by_id("dontIncluderesume").click()

            self.driver.find_element_by_id("dontIncludecoverLetter").click()
            self.driver.find_element_by_xpath("//button[@type='button'][@data-testid='continue-button-desktop']").click()

            WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH, "//a[@data-testid = 'back-button-desktop']")))
            self.driver.implicitly_wait(2)
            self.driver.find_element_by_xpath("//button[@type='button'][@data-testid='continue-button-desktop']").click()

            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//button[@type = 'submit']")))
            self.driver.find_element_by_xpath("//button[@type = 'submit']").click()
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "_2tfj6Sf")))
            if self.driver.find_element_by_class_name("_2QIfI_2"):
                self.logger.info("Successfully applied for the job")

    # Apply for the jobs that has been scraped in the json file 
    def apply(self, url):
        
        for i,data in enumerate(self.datas.get_data()):
            job_url = url+ data['jobURL']
            self.logger.info("opening page {id}...".format(id=i))
            self.driver.get(job_url)
            
            if len(self.driver.find_elements_by_link_text("Sign in")) > 0:
                self.login()
            
            self.logger.info("page loaded successfully")
            self.applyJob()
            self.logger.info("closing page {id}...".format(id=i))
            
        self.logger.info("Applying for all the jobs complete")