# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json


class ScrapyCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ScrapyComment(scrapy.Item):
    domain = scrapy.Field()
    text = scrapy.Field()
    time = scrapy.Field()

    def save(self):
        print(self)

    def toJSON(self):
        return self.__dict__['_values']

    def __repr__(self):
        return str(self.toJSON())