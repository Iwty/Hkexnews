# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql


# 将数据写入数据库
class HkenxnewsPipeline(object):
    # def __init_    _(self):

    #     self.conn = pymysql.connect(host='localhost', port=3306,
    #                                 user='root', password='lianzizhuz', db='juchao2',
    #                                 charset="utf8")
    def process_item(self, item, spider):
        conn = pymysql.connect(host='rm-8vb5ggud8sugd77vc.mysql.zhangbei.rds.aliyuncs.com', port=3306,
                               user='fdmtdb', password='Fdmt1234!', db='fdmt_dataset',
                               charset="utf8")
        cursor = conn.cursor()
        insert_sql = "INSERT INTO hkstock_gg (公告时间, 代码, 简称, 公告标题, 文件链接, 公告类型, 公告小类, 爬取时间) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(insert_sql, (
            item["公告时间"], item["代码"], item["简称"], item["公告标题"], item["文件链接"], item["公告类型"], item['公告小类'], item["爬取时间"]))

        # print('save to mysql', item)
        conn.commit()
        cursor.close()
        conn.close()
        return item


# 将数据写入本地文件
class JSONPipeline(object):
    def process_item(self, item, spider):
        # jsonfile = spider.data_file_name
        with open("./qwer.json", 'a') as f:
            f.write(json.dumps(dict(item)))
            f.write('\n')
        return item
