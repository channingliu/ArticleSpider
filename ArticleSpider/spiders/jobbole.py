# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/'] #这里放置我们所需要爬取的URL

    def parse(self, response):
        '''
        1.获取文章列表页中的文章URL，并交给scrapy下载后并进行解析
        2.获取下一页的URL并交给scrapy进行下载，下载完成后交给parse
        '''
        #解析列表页中的所有文章的URL并交给scrapy下载后并进行解析
        post_urls = response.css('#archive ')
        #post_urls = response.xpath('//div[@id="archive"]/div/div[2]/p/a[@target="_blank"]/@href').extract()

        title = response.xpath('//*[@id="post-112239"]/div[1]/h1/text()').extract()[0]
        create_time = response.xpath('// *[@id="post-112239"]/div[2]/p/text()[1]').extract()[0].strip().replace('·','').strip()
        # 使用extract_first()避免extract()[0]列表为空时报错
        praise_nums = response.xpath('//*[@id="112239votetotal"]/text()').extract_first()
        tag = response.xpath('//*[@id="post-112239"]/div[2]/p/a[3]/text()').extract()[0]
        pass
