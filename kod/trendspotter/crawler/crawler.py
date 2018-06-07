import logging
import queue
import urllib.request
from os.path import join
from bs4 import BeautifulSoup
from .models import Domain

class Crawler:
    def __init__(self, domain:Domain, scraper, visited_page_limit=1000):
        self.domain = domain
        self.scraper = scraper
        self.visited_page_limit = visited_page_limit

    def scrape(self, url):
        logging.info("SCRAPED %(url)s", {'url': join(self.domain, url)})
        return self.scraper(self.domain, url)

    @property
    def context(self):
        return {'domain': self.domain }

    def log_start(self):
        logging.info("Started crawling on domain %(domain)s", self.context)

    def log_scrape(self, url):
        logging.info("Scraping page %(domain)s/%(url)s", self.domain, self.url)

    def log_end(self):
        logging.info("Ended crawling on domain %(domain)s", self.context)

    def crawl(self):
        to_visit = set()
        visited = set()
        
        self.log_start()
        q = queue.Queue()
        q.put("")

        while(not q.empty()):
            url = q.get()
            visited.add(url)

            next_urls = self.scrape(url)

            for other_url in next_urls:
                if(len(to_visit) <= self.visited_page_limit):
                    if(other_url not in to_visit):
                        q.put(other_url)
                        to_visit.add(other_url)

        self.log_end()



def wp_scraper(domain, url):
    link_class = ["_2PrHTUx"]
    comment_class = ["_2H53dzb"]
    full_url = domain if not url else join(domain, url)
    with urllib.request.urlopen(full_url) as response:
        page = response.read()
        soup = BeautifulSoup(page, "html.parser")
        
        references = soup.find_all(lambda tag: tag.name == 'a' 
                                            and tag.has_attr('href') 
                                            and 'http' not in tag['href'])
        comments = soup.find_all(lambda tag: tag.has_attr('class') 
                                                and comment_class in tag.get('class'))

        print(comments)
        output = [reference['href'].lstrip('/') for reference in references]
        print(output)
        return output
    return []


WP_DOMAIN = Domain(name="wiadomosci.wp.pl")

DOMAINS = [ WP_DOMAIN ]

CRAWLERS = [
    Crawler("http://www." + str(WP_DOMAIN), wp_scraper, 300),
]

def one_time_crawling(*args, **kwargs):
    pass
    # for domain in DOMAINS:
    #     domain.save()

    # logging.getLogger().setLevel(logging.INFO)
    # for crawler in CRAWLERS:
    #     crawler.crawl()