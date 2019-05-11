# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql

class Hkenxnews1Pipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='rm-8vb5ggud8sugd77vc.mysql.zhangbei.rds.aliyuncs.com', port=3306,
                               user='fdmtdb', password='Fdmt1234!', db='fdmt_dataset',
                               charset="utf8")

        cursor = conn.cursor()
        insert_sql = "INSERT INTO cn_ggt (时间, 代码, 简称, 于中央结算系统的持股量, 占已发行股份百分比) VALUES (%s,%s,%s,%s,%s)"

        cursor.execute(insert_sql, (
            item["时间"], item["代码"], item["简称"], item["于中央结算系统的持股量"], item["占已发行股份百分比"]))

        # print('save to mysql', item)
        conn.commit()
        cursor.close()
        conn.close()
        return item


class JSONPipeline(object):
    def process_item(self, item, spider):
        # jsonfile = spider.data_file_name
        with open("./qwer.json", 'a') as f:
            f.write(json.dumps(dict(item)))
            f.write('\n')
        return item
