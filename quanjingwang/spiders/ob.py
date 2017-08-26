# -*- coding: utf-8 -*-
import scrapy
from quanjingwang.items import SearchListItem



class ObSpider(scrapy.Spider):
    name = 'ob'
    allowed_domains = ['www.guancha.cn']
    start_urls = ['http://www.guancha.cn/Search/?k=%E5%B0%8F%E7%B1%B3&y=1&ps=20&pi=1']

    # def start_requests(self):
    #     yield scrapy.Request(self.start_urls[0], callback=self.parse, headers=headers_o())

    def parse(self, response):
        for sel in response.xpath('//dl[@class="search-list"]/dd'):

            if sel:
                # is_ha = True
                item = SearchListItem()
                item['title'] = sel.xpath('h4/a/text()').extract()
                title = sel.xpath('h4/a/text()').extract()
                print(title)
                yield item
            else:
                return