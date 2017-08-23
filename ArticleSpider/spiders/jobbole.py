# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112239/'] #这里放置我们所需要爬取的URL

    def parse(self, response):
        title = response.xpath('//*[@id="post-112239"]/div[1]/h1/text()').extract()[0]
        create_time = response.xpath('// *[@id="post-112239"]/div[2]/p/text()[1]').extract()[0].strip().replace('·','').strip()
        # 使用extract_first()避免extract()[0]列表为空时报错
        praise_nums = response.xpath('//*[@id="112239votetotal"]/text()').extract_first()
        tag = response.xpath('//*[@id="post-112239"]/div[2]/p/a[3]/text()').extract()[0]
        pass
