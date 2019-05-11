# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Hkenxnews3Item(scrapy.Item):
    # define the fields for your item here like:
    时间 = scrapy.Field()
    代码 = scrapy.Field()
    简称 = scrapy.Field()
    持股人类别 = scrapy.Field()
    于中央结算系统的持股量 = scrapy.Field()
    参与人数目 = scrapy.Field()
    占已发行股份权证单位百分比 = scrapy.Field()
    已发行股份登记单位 = scrapy.Field()
