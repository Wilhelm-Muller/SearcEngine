# This is a scraper method that scrape most neccessary information from each html
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class HTMLobj:
    crawled_url = set()
    def __init__(self):
        self.title = ""
        self.url = ""
        self.last_mod_date = ""
        self.file_size = 0
        self.kw_freq = [] #This should be an array or set of tuples
        self.child_link = []
        self.parent_link = []
        self.link_queue = []

    def __init__(self, url): # The scraping process
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        self.child_link = []
        self.parent_link = []
        
        # Extract title, url, last mod date and file size
        self.title = soup.find('title').text
        self.url = url
        if response.status_code == 200: #successful => 200
            self.file_size = len(response.content)
            self.last_mod_date = response.headers.get('last-modified')
        
        # handling <a> tags and extract parent and children link
        link_tags = soup.find_all("a")
        links = [link.get('href') for link in link_tags]
        full_links = [urljoin(response.url, link) for link in links]
        self.link_queue = [full_link for full_link in full_links]
        url_cleaned = response.url.split(".htm")[0].strip()

        for link in full_links:
            if link.startswith(url_cleaned):
                self.child_link.append(link)
            if response.url.startswith(link.split(".htm")[0].strip()):
                self.parent_link.append(link)

    def display(self):
        print(f"Page Title: {self.title}")
        print(f"URL: {self.url}")
        print(f"Last modification date: {self.last_mod_date} | Size of Page: {self.file_size}B")
        print(f"Keyword frequency:") # Placeholder here for now
        print(f"Child Links: {self.child_link}")
        print(f"Parent Links: {self.parent_link}")
        print("-------------------------------------------------------------------")
    
class HTML_list:
    crawled_list = set()
    MAX = 30

    def __init__(self):
       self.HTML_list = [] # list of HTMLobj for later sorting

    def get_object_at(self, idx):
        try: 
            return self.HTML_list[idx]
        except:
            print("Error: Invalid argument")
            return 0
    
    def crawl(self, url):
        if len(self.crawled_list) == 30:
            return
        if url in self.crawled_list:
            pass
        else:
            Info = HTMLobj(url)
            self.crawled_list.add(url)
            self.HTML_list.append(Info)
            for link in Info.link_queue:
                self.crawl(link)
    
    # sort the HTML list by index
    def sort_by_index():
        print("Placeholder: Sort by index")
    
    # output the search result with HTMLobj's display function, will be modified to output to a text file
    def export(self):
        for page in self.HTML_list:
            page.display()
        print(f"Web crawling finished, {len(self.HTML_list)} results found.")

    
    

# Testing the crawler
A = HTML_list()
A.crawl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm")
A.export()
