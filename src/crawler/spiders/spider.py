# coding: utf-8
import scrapy

from crawler.items import Page
import settings


class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = [settings.START_URL]

    def parse(self, response):
        yield Page(url=response.url, type=response.headers['Content-Type'], body=response.body)

        # 提取本页中的图片
        queries = ['img::attr(src)', 'a[href*=".jpg"]::attr(href)', 'a[href*=".png"]::attr(href)']
        for query in queries:
            for src in response.css(query).extract():
                yield response.follow(src, self.dump)

        # 提取本页中的文本资源
        queries = ['script::attr(src)', 'link::attr(href)']
        for query in queries:
            for src in response.css(query).extract():
                    yield response.follow(src, self.dump)

        # 爬行
        # for href in response.css('a::attr(href)').extract():
        #     yield response.follow(href)

    def dump(self, response):
        yield Page(url=response.url, type=response.headers['Content-Type'], body=response.body)
