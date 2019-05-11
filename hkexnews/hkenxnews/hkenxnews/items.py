# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HkenxnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 当前字段必须和spider字段相对应,否则会报错
    公告时间 = scrapy.Field()  # 发放日期
    代码 = scrapy.Field()  # 发放时间
    简称 = scrapy.Field()  #
    公告标题 = scrapy.Field()
    文件链接 = scrapy.Field()
    公告类型 = scrapy.Field()
    公告小类 = scrapy.Field()
    爬取时间 = scrapy.Field()
