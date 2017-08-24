# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse #在py2.7中 用法：import urlparse


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
        #1.解析所有的URL
        post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        #post_urls = response.xpath('//div[@id="archive"]/div/div[2]/p/a[@target="_blank"]/@href').extract()
        #2.下载URL
        for post_url in post_urls:
            yield Request(post_url, callback=self.parse_detail)
            #有些网站的只有子域名，在提取的时候需要全域名（主域名+子域名）给parse。可用下面提供的方法：
            #request(URL = parse.urljoin(response.url,post_url),callback = self.parse_detail)
            print (post_url)

        #提取下一页，并给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(post_url, callback=self.parse)

    #parse的回调函数
    def parse_detail(self, response):
        #提取文章的目标内容
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()[1]').extract()[0].strip().replace('·','').strip()
        # 使用extract_first()避免extract()[0]列表为空时报错
        praise_nums = response.css('h10::text').extract_first() #点赞
        fav_nums = response.css('.bookmark-btn::text').extract()[0] #收藏
        match_re = re.match(r".*?(\d+).*",fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        else:
            fav_nums = 0
        #评论
        comments_nums = response.css('a[href="#article-comment"] span::text').extract()[0]
        match_re1 = re.match(r".*?(\d+).*", comments_nums)
        if match_re1:
            comments_nums = match_re1.group(1)
        else:
            comments_nums = 0

        tag = response.css('.breadcrumb-wrapper .category::text').extract()[0]
        pass
