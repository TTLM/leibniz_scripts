import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import json
import time

class DocScraper:
    def __init__(self, config):
        self.config = config
        self.driver = webdriver.Chrome()
        self.urls = []

    def load(self, url_list):
        with open(url_list, 'r') as f:
            raw_urls = json.load(f)
            self.urls = raw_urls['urls']
        return self.urls

    # def download_single_doc(self, url):
    #     self.driver.get(url)
    #     soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    # def download_one_page(self):
    #     None

    def download_pdf(self, url, save_path):
        # Send a GET request to the PDF URL
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        # Write the content of the response to a file
        with open(save_path, 'wb') as f:
            f.write(response.content)

    def scrape_doc(self, page_url):
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_element = soup.find('span', class_="tx-dlf-toc-title")
        title = title_element.get_text()
        # Extract PDF links
        pdf_links = {
            "single_page": None,
            "whole_work": None
        }

        pdf_section = soup.find('div', class_='tx-dlf-toolbox')
        if pdf_section:
            # single_page_link = pdf_section.find('span', class_='tx-dlf-tools-pdf-page').find('a')
            whole_work_link = pdf_section.find('span', class_='tx-dlf-tools-pdf-work').find('a')
            
            # if single_page_link and single_page_link['href']:
            #     pdf_links['single_page'] = single_page_link['href']
            if whole_work_link and whole_work_link['href']:
                pdf_links['whole_work'] = whole_work_link['href']
        
        # Whole work
        save_path = os.path.join(self.config.DOWNLOAD_FOLDER, title)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_path_whole = os.path.join(save_path, title + ".pdf")
        self.download_pdf(pdf_links['whole_work'], save_path_whole)

    def scrape_all_docs(self, urls):
        for url in urls:
            self.scrape_doc(url)
            print("Downloaded " + url)
            time.sleep(1)

    def split_pages(self, data_folder, filename):
        pdf_path = os.path.join(data_folder, filename, filename + ".pdf")
        if os.path.exists(pdf_path):
            pdf = PdfFileReader(pdf_path)
            for page in range(len(pdf.pages)):
                writer = PdfFileWriter()
                page_filename=filename + page + ".pdf"
                with open(page_filename, 'wb') as f:
                    writer.write(f)
            print('Created: {}'.format(page_filename))

    def split_all(self, data_folder):
        dir_list = os.listdir(data_folder)
        for dir in dir_list:
            self.split_pages(data_folder, dir)




