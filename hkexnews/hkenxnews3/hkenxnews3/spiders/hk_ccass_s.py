# !/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json
from hkenxnews3.items import Hkenxnews3Item


class HkCcassSSpider(scrapy.Spider):
    name = 'hk_ccass_s'
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
            "Cookie": "TS0161f2e5=017038eb493a2d50fd9115ca84984d0d648d90989ba691752b9ca0afcd24c4d0496c2826c0; WT_FPC=id=113.116.143.245-3490173056.30733814:lv=1557044304823:ss=1557042753323",
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
        dates = [
                 # "2018/06/11",
                 # "2018/06/12",
                 # "2018/06/13",
                 # "2018/06/14",
                 # "2018/06/15",
                 # "2018/06/16",
                 # "2018/06/18",
                 # "2018/06/19",
                 # "2018/06/20",
                 # "2018/06/21",
                 # "2018/06/22",
                 # "2018/06/23",
                 # "2018/06/25",
                 # "2018/06/26",
                 # "2018/06/27",
                 # "2018/06/28",
                 # "2018/06/29",
                 # "2018/06/30",
                 # "2018/07/02",
                 # "2018/07/03",
                 # "2018/07/04",
                 # "2018/07/05",
                 # "2018/07/06",
                 # "2018/07/07",
                 # "2018/07/09",
                 # "2018/07/10",
                 # "2018/07/11",
                 # "2018/07/12",
                 # "2018/07/13",
                 # "2018/07/14",
                 # "2018/07/16",
                 # "2018/07/17",
                 # "2018/07/18",
                 # "2018/07/19",
                 # "2018/07/20",
                 # "2018/07/21",
                 # "2018/07/23",
                 # "2018/07/24",
                 # "2018/07/25",
                 # "2018/07/26",
                 # "2018/07/27",
                 # "2018/07/28",
                 # "2018/07/30",
                 # "2018/07/31",
                 # "2018/08/01",
                 # "2018/08/02",
                 # "2018/08/03",
                 # "2018/08/04",
                 # "2018/08/06",
                 # "2018/08/07",
                 # "2018/08/08",
                 # "2018/08/09",
                 # "2018/08/10",
                 # "2018/08/11",
                 # "2018/08/13",
                 # "2018/08/14",
                 # "2018/08/15",
                 # "2018/08/16",
                 # "2018/08/17",
                 # "2018/08/18",
                 # "2018/08/20",
                 # "2018/08/21",
                 # "2018/08/22",
                 # "2018/08/23",
                 # "2018/08/24",
                 # "2018/08/25",
                 # "2018/08/27",
                 # "2018/08/28",
                 # "2018/08/29",
                 # "2018/08/30",
                 # "2018/08/31",
                 # "2018/09/01",
                 # "2018/09/03",
                 # "2018/09/04",
                 # "2018/09/05",
                 # "2018/09/06",
                 # "2018/09/07",
                 # "2018/09/08",
                 # "2018/09/10",
                 # "2018/09/11",
                 # "2018/09/12",
                 # "2018/09/13",
                 # "2018/09/14",
                 # "2018/09/15",
                 # "2018/09/17",
                 # "2018/09/18",
                 # "2018/09/19",
                 # "2018/09/20",
                 # "2018/09/21",
                 # "2018/09/22",
                 # "2018/09/24",
                 # "2018/09/25",
                 # "2018/09/26",
                 # "2018/09/27",
                 # "2018/09/28",
                 # "2018/09/29",
                 # "2018/10/01",
                 # "2018/10/02",
                 # "2018/10/03",
                 # "2018/10/04",
                 # "2018/10/05",
                 # "2018/10/06",
                 # "2018/10/08",
                 # "2018/10/09",
                 # "2018/10/10",
                 # "2018/10/11",
                 # "2018/10/12",
                 # "2018/10/13",
                 # "2018/10/15",
                 # "2018/10/16",
                 # "2018/10/17",
                 # "2018/10/18",
                 # "2018/10/19",
                 # "2018/10/20",
                 # "2018/10/22",
                 # "2018/10/23",
                 # "2018/10/24",
                 # "2018/10/25",
                 # "2018/10/26",
                 # "2018/10/27",
                 # "2018/10/29",
                 # "2018/10/30",
                 # "2018/10/31",
                 # "2018/11/01",
                 # "2018/11/02",
                 # "2018/11/03",
                 # "2018/11/05",
                 # "2018/11/06",
                 # "2018/11/07",
                 # "2018/11/08",
                 # "2018/11/09",
                 # "2018/11/10",
                 # "2018/11/12",
                 # "2018/11/13",
                 # "2018/11/14",
                 # "2018/11/15",
                 # "2018/11/16",
                 # "2018/11/17",
                 # "2018/11/19",
                 # "2018/11/20",
                 # "2018/11/21",
                 # "2018/11/22",
                 # "2018/11/23",
                 # "2018/11/24",
                 # "2018/11/26",
                 # "2018/11/27",
                 # "2018/11/28",
                 # "2018/11/29",
                 # "2018/11/30",
                 # "2018/12/01",
                 # "2018/12/03",
                 # "2018/12/04",
                 # "2018/12/05",
                 # "2018/12/06",
                 # "2018/12/07",
                 # "2018/12/08",
                 # "2018/12/10",
                 # "2018/12/11",
                 # "2018/12/12",
                 # "2018/12/13",
                 # "2018/12/14",
                 # "2018/12/15",
                 # "2018/12/17",
                 # "2018/12/18",
                 # "2018/12/19",
                 # "2018/12/20",
                 # "2018/12/21",
                 # "2018/12/22",
                 # "2018/12/24",
                 # "2018/12/25",
                 # "2018/12/26",
                 # "2018/12/27",
                 # "2018/12/28",
                 # "2018/12/29",
                 # "2018/12/31",
                 # "2019/01/01",
                 # "2019/01/02",
                 # "2019/01/03",
                 # "2019/01/04",
                 # "2019/01/05",
                 # "2019/01/07",
                 # "2019/01/08",
                 # "2019/01/09",
                 # "2019/01/10",
                 # "2019/01/11",
                 # "2019/01/12",
                 # "2019/01/14",
                 # "2019/01/15",
                 # "2019/01/16",
                 # "2019/01/17",
                 # "2019/01/18",
                 # "2019/01/19",
                 # "2019/01/21",
                 # "2019/01/22",
                 # "2019/01/23",
                 # "2019/01/24",
                 # "2019/01/25",
                 # "2019/01/26",
                 # "2019/01/28",
                 # "2019/01/29",
                 # "2019/01/30",
                 # "2019/01/31",
                 # "2019/02/01",
                 # "2019/02/02",
                 # "2019/02/04",
                 # "2019/02/05",
                 # "2019/02/06",
                 # "2019/02/07",
                 # "2019/02/08",
                 # "2019/02/09",
                 # "2019/02/11",
                 # "2019/02/12",
                 # "2019/02/13",
                 # "2019/02/14",
                 # "2019/02/15",
                 # "2019/02/16",
                 # "2019/02/18",
                 # "2019/02/19",
                 # "2019/02/20",
                 # "2019/02/21",
                 # "2019/02/22",
                 # "2019/02/23",
                 # "2019/02/25",
                 # "2019/02/26",
                 # "2019/02/27",
                 # "2019/02/28",
                 # "2019/03/01",
                 # "2019/03/02",
                 # "2019/03/04",
                 # "2019/03/05",
                 # "2019/03/06",
                 # "2019/03/07",
                 # "2019/03/08",
                 # "2019/03/09",
                 # "2019/03/11",
                 # "2019/03/12",
                 # "2019/03/13",
                 # "2019/03/14",
                 # "2019/03/15",
                 # "2019/03/16",
                 # "2019/03/18",
                 # "2019/03/19",
                 # "2019/03/20",
                 # "2019/03/21",
                 # "2019/03/22",
                 # "2019/03/23",
                 # "2019/03/25",
                 # "2019/03/26",
                 # "2019/03/27",
                 # "2019/03/28",
                 # "2019/03/29",
                 # "2019/03/30",
                 # "2019/04/01",
                 # "2019/04/02",
                 # "2019/04/03",
                 # "2019/04/04",
                 # "2019/04/05",
                 # "2019/04/06",
                 # "2019/04/08",
                 # "2019/04/09",
                 # "2019/04/10",
                 # "2019/04/11",
                 # "2019/04/12",
                 # "2019/04/13",
                 # "2019/04/15",
                 # "2019/04/16",
                 # "2019/04/17",
                 # "2019/04/18",
                 # "2019/04/19",
                 # "2019/04/20",
                 # "2019/04/22",
                 # "2019/04/23",
                 # "2019/04/24",
                 # "2019/04/25",
                 # "2019/04/26",
                 # "2019/04/27",
                 # "2019/04/29",
                 # "2019/04/30",
                 # "2019/05/01",
                 # "2019/05/02",
                 # "2019/05/03",
                 # "2019/05/04",
                 # "2019/05/06",
                 # "2019/05/07"
                 ]
        for date in dates:
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
                    "txtShareholdingDate": date,
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
        # item = response.meta["item"]
        item = Hkenxnews3Item()
        try:
            item['时间'] = response.xpath("//div[@class='filter__inputGroup']/ul/li[1]/div/input/@value").extract_first()
            item['代码'] = response.xpath("//div[@class='filter__inputGroup']/ul/li[2]/div/div/input/@value").extract_first()
            item['简称'] = response.xpath("//div[@class='filter__inputGroup']/ul/li[3]/div/div/input/@value").extract_first()
            item['已发行股份登记单位'] = response.xpath("//*[@class='summary-value']/text()").extract_first().replace(',', '')
            li_list = response.xpath("//div[contains(@class, 'ccass-search-datarow')]")
            # print(len(li_list))
            # if len(li_list) == 6:
            for li in li_list:
                # try:
                # item['时间'] = re.findall(r': (.*)', date)[0]
                # item['代码'] = li.xpath("./td[1]/div[2]/text()").extract_first()
                # item['简称'] = li.xpath("./td[2]/div[2]/text()").extract_first()
                item['持股人类别'] = li.xpath("./div[1]/text()").extract_first().strip() if li.xpath("./div[1]/text()").extract_first() else None
                item['于中央结算系统的持股量'] = li.xpath("./div[2]/div[2]/text()").extract_first().replace(',', '') if li.xpath("./div[2]/div[2]/text()").extract_first() else None
                item['参与人数目'] = li.xpath("./div[3]/div[2]/text()").extract_first().replace(',', '') if li.xpath("./div[3]/div[2]/text()").extract_first() else None
                item['占已发行股份权证单位百分比'] = "%0.4f" % (float(li.xpath("./div[4]/div[2]/text()").extract_first().split('%')[0])/100)
                # if item['占已发行股份权证单位百分比'] is None:
                #     continue
                # data = response.xpath("//*[@id='pnlResultSummary']/div/div[6]/div[2]/text()").extract_first()
                # item['已發行股份權證單位'] = re.findall(r"data='(.*?)'", data)[0] if re.findall(r"data='(.*?)'", data)[0] is None else None
                # print(item)
                yield item
        except:
            with open("./question.txt", 'a') as f:
                f.write(json.dumps(dict(item)))
                f.write('\n')
        # elif len(li_list) == 5:
        #     pass
        #         # except ValueError:
        #         #     with open("./time-time.json", 'a') as f:
        #         #         f.write(json.dumps(dict(item)))
        #         #         f.write('\n')
        # else:
        #     for li in li_list[1:-1]:
        #         # try:
        #             # item['时间'] = re.findall(r': (.*)', date)[0]
        #             # item['代码'] = li.xpath("./td[1]/div[2]/text()").extract_first()
        #             # item['简称'] = li.xpath("./td[2]/div[2]/text()").extract_first()
        #         item['持股人类别'] = li.xpath("./div[1]/text()").extract_first().strip() if li.xpath(
        #             "./div[1]/text()").extract_first() else None
        #         item['于中央结算系统的持股量'] = li.xpath("./div[2]/div[2]/text()").extract_first().replace(',', '') if li.xpath(
        #             "./div[2]/div[2]/text()").extract_first() else None
        #         item['参与人数目'] = li.xpath("./div[3]/div[2]/text()").extract_first() if li.xpath(
        #             "./div[3]/div[2]/text()").extract_first() else None
        #         item['占已发行股份权证单位百分比'] = None if item['持股人类别'] is None else ("%0.4f" % (float(li.xpath("./div[4]/div[2]/text()").extract_first().split('%')[0]) / 100))
        #             # data = response.xpath("//*[@id='pnlResultSummary']/div/div[6]/div[2]/text()").extract_first()
        #             # item['已發行股份權證單位'] = re.findall(r"data='(.*?)'", data)[0] if re.findall(r"data='(.*?)'", data)[0] is None else None
        #             # print(item)
        #         yield item
        #         # except ValueError:
        #         #     with open("./time-time.json", 'a') as f:
        #         #         f.write(json.dumps(dict(item)))
        #         #         f.write('\n')
