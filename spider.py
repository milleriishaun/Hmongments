from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Spider:

    # Class variables(shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    
    def boot(self):
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    # Function to connect to site,
    # takes html, converts proper string 
    # passes it on to LinkFinder,
    # gets a set of all the URLs and then
    # the list of the URLs can be manipulated thereafter
    def gather_links(page_url):
        # store string after decode bytes
        html_string = ''
        # whenever doing network or server operation,
        # run it within a try/except model
        try:
            response = urlopen(page_url)
            # check if HTML file, rather than pdf or something
            if 'text/html' in response.getheader('Content-Type'):
                # bytes from the ethernet cable
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            # what if connecting to a lin to page that isn't there anymore
            # we don't want to crash program, just push error
            print(str(e))
            # just return set, which is empty
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            # don't crawl the entire internet
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)
    
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    