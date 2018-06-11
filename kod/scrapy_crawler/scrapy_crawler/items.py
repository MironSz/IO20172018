# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json
import crawler.models as models
from scrapy_djangoitem import DjangoItem


class DjangoDomain(DjangoItem):
    django_model = models.Domain

class DjangoComment(DjangoItem):
    django_model = models.Comment

class DjangoWord(DjangoItem):
    django_model = models.Word

class DjangoWordOccurence(DjangoItem):
    django_model = models.WordOccurence


def remove(text, signs):
    for sign in signs:
        text = text.replace(sign, ' ')

class ScrapyComment(scrapy.Item):
    domain = scrapy.Field()
    text = scrapy.Field()
    time = scrapy.Field()


    def save(self):
        com = DjangoComment(time=self.time, domain=self.domain)
        com.save()
        words = remove(self.text, ['.', ',', '?', '!']).split(' ')
        for i, word in enumerate(words):
            word_obj = DjangoWord.objects.get(word=word)
            if not word_obj:
                word_obj = DjangoWord(word=word)
                word_obj.save()

            wordocc = DjangoWordOccurence(comment=com, place=i, word=word_obj)
            wordocc.save()

    def toJSON(self):
        return self.__dict__['_values']

    def __repr__(self):
        return str(self.toJSON())