# -*- coding: utf-8 -*-
# pycharm 不支持调试scrapy，这里新建mian.py用于调试

from scrapy.cmdline import execute
import sys
import os
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy','crawl','jobbole']) # 相当于在cmd 执行 scrapy crawl jobbole