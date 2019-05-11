# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Hkenxnews1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    时间 = scrapy.Field()
    代码 = scrapy.Field()
    简称 = scrapy.Field()
    于中央结算系统的持股量 = scrapy.Field()
    占已发行股份百分比 = scrapy.Field()
