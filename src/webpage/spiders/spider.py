# coding: utf-8
import re

import scrapy

from webpage.items import WebpageItem
import settings


class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = [settings.START_URL]

    def parse(self, response):
        yield from self.dump_text(response)

        # 提取本页中的文本资源
        queries = ['script::attr(src)', 'link::attr(href)']
        for query in queries:
            for src in response.css(query).extract():
                yield response.follow(src, self.dump_text, priority=4)

        # 提取本页中的图片
        queries = ['img::attr(src)', 'a[href*=".jpg"]::attr(href)', 'a[href*=".png"]::attr(href)']
        for query in queries:
            for src in response.css(query).extract():
                yield response.follow(src, self.dump_body, priority=2)

        # 爬行
        for href in response.css('a::attr(href)').extract():
            url = response.urljoin(href)
            if self.start_urls[0] in url:
                # 对于html资源，我们忽略其url上的参数
                url = re.sub(r'\?.*', '', url)
                yield response.follow(url)

    def dump(self, response, body):
        # https://doc.scrapy.org/en/latest/topics/request-response.html?highlight=request#scrapy.http.Response
        # response.headers 中的值不应该是 str 类型吗？
        return WebpageItem(url=response.url,
                           type=response.headers['Content-Type'].decode(),
                           body=body)

    def dump_body(self, response):
        yield self.dump(response, response.body)

    def dump_text(self, response):
        yield self.dump(response, response.text)
