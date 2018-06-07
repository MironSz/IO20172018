from django.contrib import admin
from . import crawler
# Register your models here.

crawler.one_time_crawling()