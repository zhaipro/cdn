# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebpageItem(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()
    body = scrapy.Field()
