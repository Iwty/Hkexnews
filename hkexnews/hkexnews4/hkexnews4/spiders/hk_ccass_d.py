# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from copy import deepcopy
from hkexnews4.items import Hkexnews4Item


class HkCcassDSpider(scrapy.Spider):
    name = 'hk_ccass_d'
    allowed_domains = ['www.hkexnews.hk']

    # start_urls = ['http://www.hkexnews.hk/']

    def __init__(self, txt):
        self.url = "http://www.hkexnews.hk/sdw/search/searchsdw_c.aspx"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": "TS0161f2e5=017038eb493a2d50fd9115ca84984d0d648d90989ba691752b9ca0afcd24c4d0496c2826c0; WT_FPC=id=113.116.143.245-3490173056.30733814:lv=1557044304823:ss=1557042753323",
            "Host": "www.hkexnews.hk",
            "Origin": "http://www.hkexnews.hk",
            "Referer": "http://www.hkexnews.hk/sdw/search/searchsdw_c.aspx",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        self.codes = set()
        with open(txt, 'r') as f:
            for line in f.readlines():
                if len(line) > 2:
                    self.codes.add(line)

    def start_requests(self):
        req = scrapy.Request(self.url, headers=self.headers, callback=self.parse_params)
        yield req

    def parse_params(self, response):
        view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
        __VIEWSTATEGENERATOR = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        for code in self.codes:
            data = {
                "__VIEWSTATE": view_state,
                "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                "__EVENTTARGET": "btnSearch",
                "__EVENTARGUMENT": "",
                "today": time.strftime("%Y%m%d"),
                "sortBy": "shareholding",
                "sortDirection": "desc",
                "alertMsg": "",
                "txtShareholdingDate": "2019/05/07",
                "txtStockCode": code,
                "txtStockName": "",
                "txtParticipantID": "",
                "txtParticipantName": "",
                "txtSelPartID": ""
            }
            # print(data)
            yield scrapy.FormRequest(self.url, headers=self.headers, formdata=data,
                                     callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        # start_time = time.time()
        item = Hkexnews4Item()
        item['时间'] = response.xpath("//div[@class='filter__inputGroup']/ul/li[1]/div/input/@value").extract_first()
        item['代码'] = response.xpath("//div[@class='filter__inputGroup']/ul/li[2]/div/div/input/@value").extract_first()
        item['简称'] = response.xpath("//div[@class='filter__inputGroup']/ul/li[3]/div/div/input/@value").extract_first()
        # item = response.meta["item"]
        li_list = response.xpath("//*[@class='table table-scroll table-sort table-mobile-list ']/tbody/tr")
        for li in li_list:
            try:
                item['参与者编号'] = li.xpath("./td[1]/div[2]/text()").extract_first()
                item['中央结算系统参与者名称'] = li.xpath("./td[2]/div[2]/text()").extract_first()
                item['地址'] = li.xpath("./td[3]/div[2]/text()").extract_first()
                item['持股量'] = li.xpath("./td[4]/div[2]/text()").extract_first().replace(',', '')
                item['占已发行股份权证单位百分比'] = ("%0.4f" % (float(li.xpath("./td[5]/div[2]/text()").extract_first().split('%')[0])/100))
                if li.xpath("./td[5]/div[2]/text()").extract_first() == '0.00%':
                    continue
                # print(item)
                yield item
                # end_time = time.time()
                # spend_time = end_time-start_time
                # print(spend_time)
            except:
                with open("./time-time.json", 'a') as f:
                    f.write(json.dumps(dict(item)))
                    f.write('\n')
