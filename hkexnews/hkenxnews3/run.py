# !/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy import cmdline

cmdline.execute("scrapy crawl hk_ccass_s -a txt=code.txt".split())