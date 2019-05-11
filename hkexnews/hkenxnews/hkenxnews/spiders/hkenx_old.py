# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import scrapy
import time
import json

from hkenxnews.items import HkenxnewsItem


class HkenxOldSpider(scrapy.Spider):
    name = 'hkenx_old'
    allowed_domains = ['www.hkexnews.hk']

    # start_urls = ['http://www3.hkenxnews.hk/']
    # 初始化对象，TXT需要运行时传入的数据
    def __init__(self, txt):
        self.url = "http://www3.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main_c.aspx"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Content-Length": "24708",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "toggleHeadline=false; ASP.NET_SessionId=zgk3l155yh4lkp45rwdr5t55; TS0161f2e5=017038eb49a9eff619190c5b1cfb07eff1cbd89a37f9677bd9c4d360ef4892d292c279e271; WT_FPC=id=113.116.143.245-3490173056.30733814:lv=1556871573786:ss=1556870150333",
            "Host": "www3.hkexnews.hk",
            "Origin": "http://www3.hkexnews.hk",
            "Referer": "http://www3.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main_c.aspx",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        # 将导入的TXT放入set中(重复数据可以自动过滤掉)
        self.codes = set()
        with open(txt, 'r') as f:
            for line in f.readlines():
                if len(line) > 2:
                    self.codes.add(line)

    def start_requests(self):
        # 获取start_url响应结果传给parse_index
        req = scrapy.Request(self.url, headers=self.headers, callback=self.parse_index)
        yield req

    def parse_index(self, response):
        # 获取对应字段数据供POST请求使用
        view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
        __VIEWSTATEGENERATOR = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        for code in self.codes:
            data = {
                '__VIEWSTATE': view_state,
                "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                "__VIEWSTATEENCRYPTED": "",
                "ctl00$txt_today": time.strftime("%Y%m%d"),
                "ctl00$hfStatus": "ACM",
                "ctl00$hfAlert": "",
                "ctl00$txt_stock_code": code,
                "ctl00$txt_stock_name": "",
                "ctl00$rdo_SelectDocType": "rbAll",
                "ctl00$sel_tier_1": "-2",
                "ctl00$sel_DocTypePrior2006": "-1",
                "ctl00$sel_tier_2_group": "-2",
                "ctl00$sel_tier_2": "-2",
                "ctl00$ddlTierTwo": "59,1,7",
                "ctl00$ddlTierTwoGroup": "26,5",
                "ctl00$txtKeyWord": "",
                "ctl00$rdo_SelectDateOfRelease": "rbManualRange",
                "ctl00$sel_DateOfReleaseFrom_d": "06",
                "ctl00$sel_DateOfReleaseFrom_m": "05",
                "ctl00$sel_DateOfReleaseFrom_y": "2019",
                "ctl00$sel_DateOfReleaseTo_d": "06",
                "ctl00$sel_DateOfReleaseTo_m": "05",
                "ctl00$sel_DateOfReleaseTo_y": "2019",
                "ctl00$sel_defaultDateRange": "SevenDays",
                "ctl00$rdo_SelectSortBy": "rbDateTime"
            }
            # print(data)
            yield scrapy.FormRequest(self.url, headers=self.headers, formdata=data,
                                     callback=self.after_search, dont_filter=True)

    def after_search(self, response):
        # 获取第一页数据列表
        li_list = response.xpath("//table[@id='ctl00_gvMain']/tr")
        for li in li_list[1:-1]:
            item = HkenxnewsItem()
            try:
                date = str(li.xpath("./td[1]/span/text()").extract()).replace("', '", " ")
                item['公告时间'] = re.findall(r"\['(.*?)'\]", date)[0]
                item['代码'] = li.xpath("./td[2]/span/text()").extract_first()
                item['简称'] = li.xpath("./td[3]/span/text()").extract_first()
                item['公告标题'] = li.xpath("./td[4]/a/text()").extract_first()
                item['文件链接'] = "http://www3.hkexnews.hk" + li.xpath("./td[4]/a/@href").extract_first()
                sort = str(li.xpath("./td[4]/span[1]/text()").extract())
                item['公告类型'] = sort.split(' - [')[0].split("'")[1] if sort.split(' - ')[0] is not None else sort
                # if '-' not in sort:
                #     item['公告类型'] = re.findall(r"'(.*?)'", sort)[0] if '-' not in sort else None
                #     item['公告小类'] = None
                # else:
                #     continue
                item['公告小类'] = None if '-' not in sort else sort.split(' - [')[1].split("]'")[0]
                # 小类有问题，反思*
                # item['公告小类'] = sort.split(' - [')[1].split("]'")[0] if '-' in sort else None
                # item['公告小类'] = None if item['公告类型'] == sort else sort.split(' - [')[1].split("]'")[0]
                # item['公告类型'] = re.findall(r'(.*?)', sort.split(' - [')[0].split("'")[1]) if sort.split(' - ')[0] is not None else sort
                # item['公告小类'] = None if item['公告类型'] == sort else re.findall(r'(.*?)', sort.split(' - [')[1].split("]'")[0])
                item['爬取时间'] = time.strftime("%Y-%m-%d %H:%M")
                print(item)
                # print(sort)
                yield item
            except:
                with open("./time-time.json", 'a') as f:
                    f.write(json.dumps(dict(item)))
                    f.write('\n')
        # 判断是否为空，进入下一页
        if response.meta.get("num", None) == None:
            nums = response.xpath('//span[@id="ctl00_lblDisplay"]/text()').extract_first()
            m = re.match(u'^顯示第.*至.*紀錄 \\(共有 (.*?) 紀錄\\)$', nums)
            num = int(m.group(1))
            # self.logger.info(u" %s 共计 %d 条记录" % (response.meta['code'], num))
            if num >= 20:
                view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
                __VIEWSTATEGENERATOR = ''
                try:
                    __VIEWSTATEGENERATOR = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
                except:
                    __VIEWSTATEGENERATOR = ''

                __VIEWSTATEENCRYPTED = ''
                next_data = {
                    '__VIEWSTATE': view_state,
                    'ctl00$btnNext2.x': '12',
                    'ctl00$btnNext2.y': '6',
                    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                    '__VIEWSTATEENCRYPTED': ''
                }
                req = scrapy.FormRequest(self.url, formdata=next_data, headers=self.headers, callback=self.after_search,
                                         dont_filter=True)
                req.meta['num'] = num
                # req.meta['code'] = response.meta['code']
                req.meta['current'] = 1
                yield req
        else:
            # 判断当前页是否为最后一页
            # self.logger.info(u" 接下来是 %s 的 第 %d 页记录" % (response.meta['code'], response.meta['current'] + 1))
            if (response.meta['current'] + 1) * 20 < response.meta['num']:
                view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
                __VIEWSTATEGENERATOR = ''
                try:
                    __VIEWSTATEGENERATOR = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
                except:
                    __VIEWSTATEGENERATOR = ''

                __VIEWSTATEENCRYPTED = ''
                next_data = {
                    '__VIEWSTATE': view_state,
                    'ctl00$btnNext.x': '12',
                    'ctl00$btnNext.y': '6',
                    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                    '__VIEWSTATEENCRYPTED': ''
                }

                req = scrapy.FormRequest(self.url, formdata=next_data, headers=self.headers, callback=self.after_search,
                                         dont_filter=True)
                req.meta['num'] = response.meta['num']
                # req.meta['code'] = response.meta['code']
                req.meta['current'] = response.meta['current'] + 1
                yield req
