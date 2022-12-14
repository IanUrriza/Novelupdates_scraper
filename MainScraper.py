

import undetected_chromedriver.v2 as uc
import selenium
from selenium.webdriver.common.by import By

import pandas
class MainScraper:
    driver = None
    title_df= None

    def __init__(self):
        # Create driver and initialize Data Frame
        # UC to bypass cloudflare anti bot protection
        self.driver = uc.Chrome()
        self.title_df = pandas.DataFrame(columns=['title','url'])


    def search_titles(self,page:int):
        # Mostly alphabetical but does not account any new pages generated after 07/25/22
        self.driver.get(f'https://www.novelupdates.com/novelslisting/?sort=7&order=1&status=1&pg={page}')
        content = self.driver.find_elements(By.CLASS_NAME,'search_title')
        return content

 
    def parse_content(self,content):
        # Gathers all the titles and urls in the search result
        for i in content:
            link = i.find_element(By.TAG_NAME,'a')
            title = i.text
            link_str = link.get_attribute('href')
            self.title_df = self.title_df.append({'title':title,'url':link_str},ignore_index=True)

    def compile_titles(self):
        # Manual edit since driver fails from time to time due to not being the latest version
        # By 100s for easier file management
        min_page = 501
        max_page = 522
        # max_page = 500
        for i in range(min_page,max_page+1):
            # print(i)
            content = self.search_titles(i)
            self.parse_content(content)
        self.title_df.to_csv("./Novel_List/501-522.csv", sep=',',index=True)

sc = MainScraper()
sc.compile_titles()