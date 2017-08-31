# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
# 在py2.7中 用法：import urlparse
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']  # 这里放置我们所需要爬取的URL

    def parse(self, response):
        '''
        1.获取文章列表页中的文章URL，并交给scrapy下载后并进行解析目标字段
        2.获取下一页的URL并交给scrapy进行下载，下载完成后交给parse
        3.循环步骤1,2
        '''

        # 解析列表页中的所有文章的URL并交给scrapy下载后并进行解析
        # 1.解析所有的URL
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        # post_urls = response.xpath('//div[@id="archive"]/div/div[2]/p/a[@target="_blank"]/@href').extract()
        # 2.Request对获取的URL进行下载，在完成后调用自定义的解析函数
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first()
            post_url = post_node.css("::attr(href)").extract_first()
            # yield Request(post_url, callback=self.parse_detail)
            # 有些网站的只有子域名，在提取的时候需要全域名（主域名+子域名）给parse。可用下面提供的方法：
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)
            print(post_url)

        # 提取下一页，并给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(post_url, callback=self.parse)

    # parse的回调函数，提取文章的目标内容
    def parse_detail(self, response):
        # 实例化 itemes
        article_item = JobBoleArticleItem()
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()[1]').extract()[0].strip().replace('·', '').strip()
        # 使用extract_first()避免extract()[0]列表为空时报错
        praise_nums = response.css('h10::text').extract_first()  # 点赞
        fav_nums = response.css('.bookmark-btn::text').extract()[0]  # 收藏
        match_re = re.match(r".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        else:
            fav_nums = 0
        # 评论
        comment_nums = response.css('a[href="#article-comment"] span::text').extract()[0]
        match_re1 = re.match(r".*?(\d+).*", comment_nums)
        if match_re1:
            comment_nums = match_re1.group(1)
        else:
            comment_nums = 0

        tag = response.css('.breadcrumb-wrapper .category::text').extract()[0]

        article_item["title"] = title
        article_item["url"] = response.url
        article_item["create_time"] = create_time
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tag

        yield article_item  # 这里的article_item 会传送到pipelines.py中





        pass
