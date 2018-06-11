# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json
import crawler.models as models
from django.db import transaction


def remove(text, signs):
    for sign in signs:
        text = text.replace(sign, ' ')
    return text
    

class ScrapyComment(scrapy.Item):
    domain = scrapy.Field()
    text = scrapy.Field()
    time = scrapy.Field()

    @transaction.atomic
    def save(self):
        words = remove(self['text'], ['.', ',', '?', '!']).split(' ')
        words = list(filter(lambda x: x != '', words))
        
        dom_obj, created = models.Domain.objects.get_or_create(name=self['domain'])
        if created:
            dom_obj.save()

        com = models.Comment(time=self['time'], domain=dom_obj)
        com.save()

        for i, word in enumerate(words):
            word_obj, created  = models.Word.objects.get_or_create(word=word)
            if created:
                word_obj.save()

            wordocc = models.WordOccurence(comment=com, place=i, word=word_obj)
            wordocc.save()

    def toJSON(self):
        return self.__dict__['_values']

    def __repr__(self):
        return str(self.toJSON())