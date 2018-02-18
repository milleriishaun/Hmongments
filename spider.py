from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


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

    @staticmethod
    def boot(self):
        create_project_dir(Spider.project_name)
        create_data_file(Spider.project_name, Spider.base_url)
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
            if response.getheader('Content-Type') == 'text/html':
                # bytes from the ethernet cable
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            # what if connecting to a lin to page that isn't there anymore
            # we don't want to crash program, just push error
            print('Error: can not crawl page')
            # just return set, which is empty
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            # don't crawl the entire internet
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)
    
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    