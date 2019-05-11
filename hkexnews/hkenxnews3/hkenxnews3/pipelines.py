# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .GeneralHashFunctions import *
import redis
import pickle
import base64
import requests
import json
import time
import pymysql


class Hkenxnews3Pipeline(object):
    # 哈希函数列表
    hash_list = [rs_hash, js_hash, pjw_hash, elf_hash, bkdr_hash, sdbm_hash, djb_hash, dek_hash]

    def __init__(self):
        # self.key = "hk_ccass_s"
        self.redis = redis.StrictRedis(host='127.0.0.1', port=6379, charset='utf-8')

    def random_generator(self, hash_value):
        '''
        将hash函数得出的函数值映射到[0, 2^32-1]区间内
        '''
        return hash_value % (1 << 15)

    def process_item(self, item, spider):
        # items = item
        key = "hk_ccass_s"
        data = pickle.dumps(str(item["代码"]) + str(item['简称']) + str(item["持股人类别"]) + str(item['于中央结算系统的持股量']) + str(
            item['参与人数目']) + str(item['占已发行股份权证单位百分比']))
        # print(data)
        data1 = base64.b64encode(data).decode()

        """
                过滤，判断是否存在
                :param item:
                :return:
                """
        # flag = True  # 默认存在
        for hash in self.hash_list:
            # 计算哈希值
            hash_value = hash(data1)
            # 获取映射到位数组的下标值
            index_value = self.random_generator(hash_value)
            # 判断指定位置标记是否为 0
        if self.redis.getbit(key, index_value) == 0:
            time.sleep(0.5)
            # 如果不存在需要保存，则写入
            self.redis.setbit(key, index_value, 1)
            # 连接数据库，实时更新数据
            conn = pymysql.connect(host='rm-8vb5ggud8sugd77vcuo.mysql.zhangbei.rds.aliyuncs.com', port=3306,
                                   user='fdmtdb', password='Fdmt1234!', db='work_test',
                                   charset="utf8")
            # conn = pymysql.connect(host='localhost', port=3306,
            #                        user='root', password='lianzizhuz', db='juchao2',
            #                        charset="utf8")
            cursor = conn.cursor()
            insert_sql = "INSERT INTO hk_ccass_s (时间, 代码, 简称, 持股人类别, 于中央结算系统的持股量, 参与人数目, `占已发行股份/权证/单位百分比`, `已发行股份/登记/单位`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

            cursor.execute(insert_sql, (
                item["时间"], item["代码"], item["简称"], item["持股人类别"], item["于中央结算系统的持股量"], item["参与人数目"],
                item['占已发行股份权证单位百分比'], item["已发行股份登记单位"]))

            # print('save to mysql', item)
            conn.commit()
            cursor.close()
            conn.close()
            return item
        else:
            print("存在")


class JsonHkexnews3(object):
    def process_item(self, item, spider):
        # jsonfile = spider.data_file_name
        with open("./qwer.json", 'a') as f:
            f.write(json.dumps(dict(item)))
            f.write('\n')
        return item
