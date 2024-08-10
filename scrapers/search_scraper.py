from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re

class SearchScraper:
    def __init__(self, config):
        self.config = config
        self.driver = webdriver.Chrome()
        self.urls = []
        # self.metadata = []
        
    def search(self, query):
        self.driver.get(self.config.SEARCH_PAGE)
        search_box = self.driver.find_element(By.NAME, self.config.SEARCH_BOX_NAME)
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)


    def find_next(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        next_icon = soup.find('i', class_='icon-chevron-right')
        # next_button = soup.find_parent(next_icon)
        # icon_prev = soup.find_previous_sibling(next_icon)
        # icon_next = soup.find_next_sibling(next_icon)
        prev_a = next_icon.find_previous('a')
        print(next_icon)
        # print(next_button)
        # print(icon_prev)
        # print(icon_next)
        print(prev_a)


    def parse_results(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # http://digitale-sammlungen.gwlb.de/resolve?id=00068093
        pattern = re.compile(r'http://digitale-sammlungen\.gwlb\.de/resolve\?id=\d+')
        results = soup.find_all('a', href=pattern)
        self.urls.extend([link['href'] for link in results])
        # self.metadata.extend([link.get_text() for link in results])

        # Handle pagination
        next_icon = soup.find('i', class_='icon-chevron-right')
        # for i in range(3):
        while (next_icon):
            next_button = next_icon.find_previous('a')
            # next_button_url = next_button['href']
            next_button_url = self.config.BASE_URL + next_button['href']
            self.driver.get(next_button_url)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            results = soup.find_all('a', href=pattern)
            self.urls.extend([link['href'] for link in results])
            # self.metadata.extend([link.get_text() for link in results])
            next_icon = soup.find('i', class_='icon-chevron-right')

        with open(self.config.JSON_FILE, 'w') as f:
            # json.dump({"urls": self.urls, "metadata": self.metadata}, f, indent=4)
            json.dump({"urls": self.urls}, f, indent=4)

        # with open("data/search.html", 'w') as f2:
        #     f2.write(str(soup))

