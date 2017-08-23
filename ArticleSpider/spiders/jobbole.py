# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/'] #这里放置我们所需要爬取的URL，测试123

    def parse(self, response):
        pass
