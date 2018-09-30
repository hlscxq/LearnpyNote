# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Y58ErshouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    baseInfo = scrapy.Field()
    price=scrapy.Field()
    time=scrapy.Field()
    #loc = scrapy.Field()
    ageInfo=scrapy.Field()