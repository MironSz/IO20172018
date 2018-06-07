import scrapy
from scrapy_crawler.items import ScrapyComment

class WPSpider(scrapy.Spider):
    name = "wp"

    allowed_domains = [
      'wiadomosci.wp.pl'
    ]
    start_urls = [
      'https://wiadomosci.wp.pl/'
    ]

    def parse(self, response):
        """
        @returns requests 0 20
        @returns items 0 5
        """
        self.logger.info('Hi, this is an item page! %s', response.url)

        for quote in response.css('a::attr(href)'):
          yield ScrapyComment(
              domain = self.allowed_domains[0],
              text = quote,
              time = quote
          )

        # follow links
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse)