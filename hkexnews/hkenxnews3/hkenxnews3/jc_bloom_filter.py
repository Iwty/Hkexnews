# !/usr/bin/env python
# -*- coding: utf-8 -*-
from GeneralHashFunctions import *
import redis
import pickle
import base64
import requests
import json
import time
import random
import pymysql


class BloomFilterRedis(object):
    # 哈希函数列表
    hash_list = [rs_hash, js_hash, pjw_hash, elf_hash, bkdr_hash, sdbm_hash, djb_hash, dek_hash]

    # rs_hash(1)
    def __init__(self, key, cate, d, f):
        self.key = key
        self.redis = redis.StrictRedis(host='127.0.0.1', port=6379, charset='utf-8')
        self.url1 = "http://www.cninfo.com.cn/new/data/list-search.json"
        self.url2 = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
        self.headers1 = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice-szse-main",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.headers2 = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            # "Content-Length": "134",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "JSESSIONID=A8784B7FFB4DE75CE270DC4BD092E3E8; JSESSIONID=A8784B7FFB4DE75CE270DC4BD092E3E8; cninfo_user_browse=000002,gssz0000002,%E4%B8%87%20%20%E7%A7%91%EF%BC%A1; _sp_ses.2141=*; _sp_id.2141=d9b9db3e-ebc5-4307-a374-064683e30af9.1553658423.31.1555925496.1555920220.92290934-eafa-49a7-ba88-c9bf76529e02",
            "Host": "www.cninfo.com.cn",
            "Origin": "http://www.cninfo.com.cn",
            "Referer": "http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice-szse-main",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.parsms = {
            "pageNum": 1,
            "pageSize": "50",
            "tabName": "relation",
            "column": "szse",
            "stock": "",
            "searchkey": "",
            "secid": "",
            "plate": "sz",
            "category": cate,
            "trade": "",
            "seDate": "%s ~ %s" % (d, f)
            # "seDate": "2019-04-26"
            # date = time.strftime("%Y-%m-%d~%H:%M:%S"))
        }
        # print(self.parsms)

    def start_requests(self, sort):
        resp = requests.post(self.url2, headers=self.headers2, params=self.parsms)
        result = json.loads(resp.text)
        # time.sleep(1)
        # print(result)
        for dat in result["announcements"]:
            # print(dat)
            # try:
            item = {}
            # item['code'] = dat['secCode']
            # try:
            # item['name'] = dat['secName']

            item['代码'] = dat['secCode']
            item['简称'] = dat['secName']

            item['公告标题'] = dat['announcementTitle']
            item['公告链接'] = 'http://static.cninfo.com.cn/' + dat['adjunctUrl']

            timeStamp = int(dat['announcementTime'])
            timeStamp /= 1000.0
            timearr = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d~%H:%M:%S", timearr)
            # print otherStyleTime
            item['公告时间'] = otherStyleTime
            item['公告类型'] = sort
            item['爬取时间'] = time.strftime("%Y-%m-%d~%H:%M")
            # print(item)
            items = item
            data = pickle.dumps(str(items["代码"]) + str(items['公告标题']) + str(items["公告链接"]) + str(items['公告类型']))
            # print(data)
            data1 = base64.b64encode(data).decode()
            # print(data1)
            # time.sleep(1)

            bloom.do_filter(data1, items)

    def random_generator(self, hash_value):
        '''
        将hash函数得出的函数值映射到[0, 2^32-1]区间内
        '''
        return hash_value % (1 << 15)

    def do_filter(self, item, items):
        """
        过滤，判断是否存在
        :param item:
        :return:
        """
        # flag = True  # 默认存在
        for hash in self.hash_list:
            # 计算哈希值
            hash_value = hash(item)
            # 获取映射到位数组的下标值
            index_value = self.random_generator(hash_value)
            # 判断指定位置标记是否为 0
        if self.redis.getbit(self.key, index_value) == 0:
            time.sleep(0.5)
            # 如果不存在需要保存，则写入
            self.redis.setbit(self.key, index_value, 1)
            # 连接数据库，实时更新数据
            conn = pymysql.connect(host='rm-8vb5ggud8sugd77vc.mysql.zhangbei.rds.aliyuncs.com', port=3306,
                                   user='fdmtdb', password='Fdmt1234!', db='juchao_data',
                                   charset="utf8")

            cursor = conn.cursor()
            insert_sql = "INSERT INTO jc_master_dy (代码, 简称, 公告标题, 公告链接, 公告时间, 公告类型, 爬取时间) VALUES (%s,%s,%s,%s,%s,%s,%s)"

            cursor.execute(insert_sql, (
                items["代码"], items["简称"], items["公告标题"], items["公告链接"], items["公告时间"], items["公告类型"], items["爬取时间"]))

            # print('save to mysql', items)
            conn.commit()
            cursor.close()
            conn.close()
            # print(1)
        else:
            # no commit
            print('存在')


if __name__ == '__main__':
    a = str(time.time()).split('.')[0]
    timearr = time.localtime(int(a) - 6000)
    timearr1 = time.localtime(int(a) + 86400)
    d = (time.strftime("%Y-%m-%d", timearr))
    f = (time.strftime("%Y-%m-%d", timearr1))
    category_dict = {'category_mdcf_szdy': '媒体采访',
                     'category_lyhd_szdy': '路演活动',
                     'category_dyhd_szdy': '调研活动',
                     'category_glzd_szdy': '管理制度'
                     }
    for cate, sort in category_dict.items():
        bloom = BloomFilterRedis("jc_master_pl", cate, d, f)
        bloom.start_requests(sort)