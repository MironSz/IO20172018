import scrapy
from scrapy_crawler.items import ScrapyComment
from scrapy.selector import Selector
import scrapy_crawler.spiders.parser as parser
from scrapy_splash import SplashRequest
from .parser import extract_comment
import os


class CommentSpider(scrapy.Spider):
    lua_script = None

    def start_requests(self):
        for url in self.start_urls:
            yield self.splash_request(url)

    def splash_request(self, url):
        return SplashRequest(url=url, callback=self.parse, endpoint='execute', args ={'lua_source': self.lua_script, 'timeout': 120})

class WPSpider(CommentSpider):
    name = "wp"

    allowed_domains = [
      'wiadomosci.wp.pl'
    ]

    lua_script_path = 'wp_script.lua'

    BASE_URL = 'https://wiadomosci.wp.pl'

    start_urls = [
        BASE_URL
        #'https://wiadomosci.wp.pl/coraz-wiecej-niemcow-chce-nosic-przy-sobie-bron-hukowo-alarmowa-czuja-sie-niepewnie-6062476040389761a'
    ]

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        comments = response.__dict__['_cached_data']['comments']
        for key in comments:
            yield ScrapyComment(extract_comment(comments[key]))

        links = response.__dict__['_cached_data']['links']
        for link in links:
            print(link)
            yield self.splash_request(link)


FOLDER_PATH = 'scrapy_crawler/spiders'
with open(os.path.join(FOLDER_PATH, WPSpider.lua_script_path), 'r') as file:
    WPSpider.lua_script = file.read()