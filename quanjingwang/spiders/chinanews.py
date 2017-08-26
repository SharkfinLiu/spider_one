# -*- coding: utf-8 -*-
import scrapy
from quanjingwang.items import SearchListItem
import re


class ChinanewsSearchSpider(scrapy.Spider):
    name = 'chinanews_ChinanewsSearchSpider'
    allowed_domains = ['sou.chinanews.com']
    # dt = 20170728  # 发布时间

    def __init__(self, keyword=None, *args, **kwargs):
        super(ChinanewsSearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://sou.chinanews.com/search.do?q={0}&start=0'.format(keyword)]
        self.index = 1

    def get_next_url(self, OldUrl):
        l = OldUrl.split('=')
        NewID = int(l[2]) + 10
        NewUrl = l[0] + '=' + l[1] + '=' + str(NewID)
        return str(NewUrl)

    def parse(self, response):
        is_ha = False
        for sel in response.xpath('//div[@id="news_list"]/table'):
            try:
                if sel:
                    is_ha = True
                    item = SearchListItem()
                    item['title'] = [''.join(sel.xpath('tr[1]/td[2]/ul/li[1]/a//text()').extract())]
                    item['url'] = sel.xpath('tr[1]/td[2]/ul/li[1]/a/@href').extract()
                    item['imgs'] = sel.xpath('tr[1]/td[1]/a//img/@src').extract()
                    item['abstract'] = [''.join(sel.xpath('tr[1]/td[2]/ul/li[2]//text()').extract()).replace('\r', '').replace('\n', '').strip()]
                    content = sel.xpath('tr[2]/td/ul/li/text()').extract()
                    item['published_at'] = [content[0].replace('\t', '').split('\r\n')[-2]]
                    split_publish_at = item['published_at'][0].split(' ')
                    split_publish_at = split_publish_at[0].replace('-', '')
                    item['index'] = self.index
                    self.index += 1
                    # 发布时间控制
                    # if int(split_publish_at) < self.dt:
                    #     return
                    yield item
            except:
                print("error")
        if is_ha:
            next_Url = self.get_next_url(response.url)
            yield scrapy.Request(next_Url, callback=self.parse, dont_filter=True)
        else:
            return
