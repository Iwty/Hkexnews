# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import scrapy
import time
from hkenxnews1.items import Hkenxnews1Item


class Hkenx1Spider(scrapy.Spider):
    name = 'hkenx1'
    allowed_domains = ['www3.hkenxnews.hk']

    # start_urls = ['http://www3.hkenxnews.hk/']

    def __init__(self):
        self.url = "http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": "TS0161f2e5=017038eb490628455d2a13c6e10f7196a0e2cc461e1bebd9c3b6da8d9eea68f8a907b9b205; WT_FPC=id=113.116.143.245-3490173056.30733814:lv=1557039108710:ss=1557036636866",
            "Host": "www.hkexnews.hk",
            "Origin": "http://www.hkexnews.hk",
            "Referer": "http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        # self.dates = set()
        # with open(txt, 'r') as f:
        #     for line in f.readlines():
        #         if len(line) > 2:
        #             self.dates.add(line)

    def start_requests(self):
        req = scrapy.Request(self.url, headers=self.headers, callback=self.parse_params)
        yield req

    def parse_params(self, response):
        # 获取start_request中响应的FromData传入给data
        view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
        __VIEWSTATEGENERATOR = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        __EVENTVALIDATION = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first()
        # dates = ["2018/05/06",
        #          "2018/05/07",
        #          "2018/05/08",
        #          "2018/05/09",
        #          "2018/05/10",
        #          "2018/05/11",
        #          "2018/05/12",
        #          "2018/05/13",
        #          "2018/05/14",
        #          "2018/05/15",
        #          "2018/05/16",
        #          "2018/05/17",
        #          "2018/05/18",
        #          "2018/05/19",
        #          "2018/05/20",
        #          "2018/05/21",
        #          "2018/05/22",
        #          "2018/05/23",
        #          "2018/05/24",
        #          "2018/05/25",
        #          "2018/05/26",
        #          "2018/05/27",
        #          "2018/05/28",
        #          "2018/05/29",
        #          "2018/05/30",
        #          "2018/05/31",
        #          "2018/06/01",
        #          "2018/06/02",
        #          "2018/06/03",
        #          "2018/06/04",
        #          "2018/06/05",
        #          "2018/06/06",
        #          "2018/06/07",
        #          "2018/06/08",
        #          "2018/06/09",
        #          "2018/06/10",
        #          "2018/06/11",
        #          "2018/06/12",
        #          "2018/06/13",
        #          "2018/06/14",
        #          "2018/06/15",
        #          "2018/06/16",
        #          "2018/06/17",
        #          "2018/06/18",
        #          "2018/06/19",
        #          "2018/06/20",
        #          "2018/06/21",
        #          "2018/06/22",
        #          "2018/06/23",
        #          "2018/06/24",
        #          "2018/06/25",
        #          "2018/06/26",
        #          "2018/06/27",
        #          "2018/06/28",
        #          "2018/06/29",
        #          "2018/06/30",
        #          "2018/07/01",
        #          "2018/07/02",
        #          "2018/07/03",
        #          "2018/07/04",
        #          "2018/07/05",
        #          "2018/07/06",
        #          "2018/07/07",
        #          "2018/07/08",
        #          "2018/07/09",
        #          "2018/07/10",
        #          "2018/07/11",
        #          "2018/07/12",
        #          "2018/07/13",
        #          "2018/07/14",
        #          "2018/07/15",
        #          "2018/07/16",
        #          "2018/07/17",
        #          "2018/07/18",
        #          "2018/07/19",
        #          "2018/07/20",
        #          "2018/07/21",
        #          "2018/07/22",
        #          "2018/07/23",
        #          "2018/07/24",
        #          "2018/07/25",
        #          "2018/07/26",
        #          "2018/07/27",
        #          "2018/07/28",
        #          "2018/07/29",
        #          "2018/07/30",
        #          "2018/07/31",
        #          "2018/08/01",
        #          "2018/08/02",
        #          "2018/08/03",
        #          "2018/08/04",
        #          "2018/08/05",
        #          "2018/08/06",
        #          "2018/08/07",
        #          "2018/08/08",
        #          "2018/08/09",
        #          "2018/08/10",
        #          "2018/08/11",
        #          "2018/08/12",
        #          "2018/08/13",
        #          "2018/08/14",
        #          "2018/08/15",
        #          "2018/08/16",
        #          "2018/08/17",
        #          "2018/08/18",
        #          "2018/08/19",
        #          "2018/08/20",
        #          "2018/08/21",
        #          "2018/08/22",
        #          "2018/08/23",
        #          "2018/08/24",
        #          "2018/08/25",
        #          "2018/08/26",
        #          "2018/08/27",
        #          "2018/08/28",
        #          "2018/08/29",
        #          "2018/08/30",
        #          "2018/08/31",
        #          "2018/09/01",
        #          "2018/09/02",
        #          "2018/09/03",
        #          "2018/09/04",
        #          "2018/09/05",
        #          "2018/09/06",
        #          "2018/09/07",
        #          "2018/09/08",
        #          "2018/09/09",
        #          "2018/09/10",
        #          "2018/09/11",
        #          "2018/09/12",
        #          "2018/09/13",
        #          "2018/09/14",
        #          "2018/09/15",
        #          "2018/09/16",
        #          "2018/09/17",
        #          "2018/09/18",
        #          "2018/09/19",
        #          "2018/09/20",
        #          "2018/09/21",
        #          "2018/09/22",
        #          "2018/09/23",
        #          "2018/09/24",
        #          "2018/09/25",
        #          "2018/09/26",
        #          "2018/09/27",
        #          "2018/09/28",
        #          "2018/09/29",
        #          "2018/09/30",
        #          "2018/10/01",
        #          "2018/10/02",
        #          "2018/10/03",
        #          "2018/10/04",
        #          "2018/10/05",
        #          "2018/10/06",
        #          "2018/10/07",
        #          "2018/10/08",
        #          "2018/10/09",
        #          "2018/10/10",
        #          "2018/10/11",
        #          "2018/10/12",
        #          "2018/10/13",
        #          "2018/10/14",
        #          "2018/10/15",
        #          "2018/10/16",
        #          "2018/10/17",
        #          "2018/10/18",
        #          "2018/10/19",
        #          "2018/10/20",
        #          "2018/10/21",
        #          "2018/10/22",
        #          "2018/10/23",
        #          "2018/10/24",
        #          "2018/10/25",
        #          "2018/10/26",
        #          "2018/10/27",
        #          "2018/10/28",
        #          "2018/10/29",
        #          "2018/10/30",
        #          "2018/10/31",
        #          "2018/11/01",
        #          "2018/11/02",
        #          "2018/11/03",
        #          "2018/11/04",
        #          "2018/11/05",
        #          "2018/11/06",
        #          "2018/11/07",
        #          "2018/11/08",
        #          "2018/11/09",
        #          "2018/11/10",
        #          "2018/11/11",
        #          "2018/11/12",
        #          "2018/11/13",
        #          "2018/11/14",
        #          "2018/11/15",
        #          "2018/11/16",
        #          "2018/11/17",
        #          "2018/11/18",
        #          "2018/11/19",
        #          "2018/11/20",
        #          "2018/11/21",
        #          "2018/11/22",
        #          "2018/11/23",
        #          "2018/11/24",
        #          "2018/11/25",
        #          "2018/11/26",
        #          "2018/11/27",
        #          "2018/11/28",
        #          "2018/11/29",
        #          "2018/11/30",
        #          "2018/12/01",
        #          "2018/12/02",
        #          "2018/12/03",
        #          "2018/12/04",
        #          "2018/12/05",
        #          "2018/12/06",
        #          "2018/12/07",
        #          "2018/12/08",
        #          "2018/12/09",
        #          "2018/12/10",
        #          "2018/12/11",
        #          "2018/12/12",
        #          "2018/12/13",
        #          "2018/12/14",
        #          "2018/12/15",
        #          "2018/12/16",
        #          "2018/12/17",
        #          "2018/12/18",
        #          "2018/12/19",
        #          "2018/12/20",
        #          "2018/12/21",
        #          "2018/12/22",
        #          "2018/12/23",
        #          "2018/12/24",
        #          "2018/12/25",
        #          "2018/12/26",
        #          "2018/12/27",
        #          "2018/12/28",
        #          "2018/12/29",
        #          "2018/12/30",
        #          "2018/12/31",
        #          "2019/01/01",
        #          "2019/01/02",
        #          "2019/01/03",
        #          "2019/01/04",
        #          "2019/01/05",
        #          "2019/01/06",
        #          "2019/01/07",
        #          "2019/01/08",
        #          "2019/01/09",
        #          "2019/01/10",
        #          "2019/01/11",
        #          "2019/01/12",
        #          "2019/01/13",
        #          "2019/01/14",
        #          "2019/01/15",
        #          "2019/01/16",
        #          "2019/01/17",
        #          "2019/01/18",
        #          "2019/01/19",
        #          "2019/01/20",
        #          "2019/01/21",
        #          "2019/01/22",
        #          "2019/01/23",
        #          "2019/01/24",
        #          "2019/01/25",
        #          "2019/01/26",
        #          "2019/01/27",
        #          "2019/01/28",
        #          "2019/01/29",
        #          "2019/01/30",
        #          "2019/01/31",
        #          "2019/02/01",
        #          "2019/02/02",
        #          "2019/02/03",
        #          "2019/02/04",
        #          "2019/02/05",
        #          "2019/02/06",
        #          "2019/02/07",
        #          "2019/02/08",
        #          "2019/02/09",
        #          "2019/02/10",
        #          "2019/02/11",
        #          "2019/02/12",
        #          "2019/02/13",
        #          "2019/02/14",
        #          "2019/02/15",
        #          "2019/02/16",
        #          "2019/02/17",
        #          "2019/02/18",
        #          "2019/02/19",
        #          "2019/02/20",
        #          "2019/02/21",
        #          "2019/02/22",
        #          "2019/02/23",
        #          "2019/02/24",
        #          "2019/02/25",
        #          "2019/02/26",
        #          "2019/02/27",
        #          "2019/02/28",
        #          "2019/03/01",
        #          "2019/03/02",
        #          "2019/03/03",
        #          "2019/03/04",
        #          "2019/03/05",
        #          "2019/03/06",
        #          "2019/03/07",
        #          "2019/03/08",
        #          "2019/03/09",
        #          "2019/03/10",
        #          "2019/03/11",
        #          "2019/03/12",
        #          "2019/03/13",
        #          "2019/03/14",
        #          "2019/03/15",
        #          "2019/03/16",
        #          "2019/03/17",
        #          "2019/03/18",
        #          "2019/03/19",
        #          "2019/03/20",
        #          "2019/03/21",
        #          "2019/03/22",
        #          "2019/03/23",
        #          "2019/03/24",
        #          "2019/03/25",
        #          "2019/03/26",
        #          "2019/03/27",
        #          "2019/03/28",
        #          "2019/03/29",
        #          "2019/03/30",
        #          "2019/03/31",
        #          "2019/04/01",
        #          "2019/04/02",
        #          "2019/04/03",
        #          "2019/04/04",
        #          "2019/04/05",
        #          "2019/04/06",
        #          "2019/04/07",
        #          "2019/04/08",
        #          "2019/04/09",
        #          "2019/04/10",
        #          "2019/04/11",
        #          "2019/04/12",
        #          "2019/04/13",
        #          "2019/04/14",
        #          "2019/04/15",
        #          "2019/04/16",
        #          "2019/04/17",
        #          "2019/04/18",
        #          "2019/04/19",
        #          "2019/04/20",
        #          "2019/04/21",
        #          "2019/04/22",
        #          "2019/04/23",
        #          "2019/04/24",
        #          "2019/04/25",
        #          "2019/04/26",
        #          "2019/04/27",
        #          "2019/04/28",
        #          "2019/04/29",
        #          "2019/04/30",
        #          "2019/05/01",
        #          "2019/05/02",
        #          "2019/05/03",
        #          "2019/05/04",
        #          "2019/05/05",
        #          "2019/05/06"
        #          ]
        dates = ["2019/05/06"]
        for date in dates:
            data = {
                "__VIEWSTATE": view_state,
                "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                "__EVENTVALIDATION": __EVENTVALIDATION,
                "today": time.strftime("%Y%m%d"),
                "sortBy": "stockcode",
                "sortDirection": "asc",
                "alertMsg": "",
                "txtShareholdingDate": date,
                "btnSearch": "搜尋"
            }
            # 发送POST请求
            yield scrapy.FormRequest(self.url, headers=self.headers, formdata=data,
                                     callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        date = response.xpath("//div[@id='pnlResult']/h2/span/text()").extract_first()
        li_list = response.xpath("//table[@id='mutualmarket-result']/tbody/tr")
        for li in li_list:
            item = Hkenxnews1Item()
            try:
                item['时间'] = re.findall(r': (.*)', date)[0]
                item['代码'] = li.xpath("./td[1]/div[2]/text()").extract_first()
                item['简称'] = li.xpath("./td[2]/div[2]/text()").extract_first()
                item['于中央结算系统的持股量'] = li.xpath("./td[3]/div[2]/text()").extract_first()
                item['占已发行股份百分比'] = li.xpath("./td[4]/div[2]/text()").extract_first()
                # print(item)
                yield item
            except ValueError:
                print(111111111111111)
