# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql


class Hkexnews4Pipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='rm-8vb5ggud8sugd77vcuo.mysql.zhangbei.rds.aliyuncs.com', port=3306,
                               user='fdmtdb', password='Fdmt1234!', db='work_test',
                               charset="utf8")
        # conn = pymysql.connect(host='localhost', port=3306,
        #                        user='root', password='lianzizhuz', db='juchao2',
        #                        charset="utf8")
        cursor = conn.cursor()
        insert_sql = "INSERT INTO hk_ccass_d5 (时间, 代码, 简称, 参与者编号, 中央结算系统参与者名称, 地址, 持股量, `占已发行股份/权证/单位百分比`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(insert_sql, (
            item["时间"], item["代码"], item["简称"], item["参与者编号"], item["中央结算系统参与者名称"], item["地址"], item['持股量'],
            item["占已发行股份权证单位百分比"]))

        # print('save to mysql', item)
        conn.commit()
        cursor.close()
        conn.close()
        return item


class JsonHkexnews4(object):
    def process_item(self, item, spider):
        # jsonfile = spider.data_file_name
        with open("./qwer.json", 'a', encoding="utf-8") as f:
            f.write(json.dumps(dict(item)))
            f.write('\n')
        return item
