# !/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy import cmdline

#cmdline.execute("scrapy crawl search_by_days -a txt=master.txt -a datafile=begin.json -a days=3".split())
cmdline.execute("scrapy crawl hkenx_old -a txt=code.txt".split())
# cmdline.execute("scrapy crawl hkenx_old".split())
