# -*- coding: utf-8 -*-
# pycharm 不支持调试scrapy，这里新建mian.py用于调试

from scrapy.cmdline import execute
import sys
import os
print(os.path.dirname(os.path.abspath(__file__)))
# 需要设置爬虫工程目录，运行main.py时，execute才会生效
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 下面语句相当于在cmd 执行 scrapy crawl jobbole
execute(['scrapy', 'crawl', 'jobbole'])