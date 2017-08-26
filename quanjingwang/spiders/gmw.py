# -*- coding: utf-8 -*-
import scrapy
from quanjingwang.items import SearchListItem
import re


class GmwSeacherSpider(scrapy.Spider):
    name = 'gmw_GmwSeacherSpider'
    allowed_domains = ['search.gmw.cn']
    dt = 20170822  # 发布时间
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         'quanjingwang.pipelines.Scrapy_gmw_dataPipeline': 300,
    #     },
    #
    # }

    def __init__(self, keyword=None, *args, **kwargs):
        super(GmwSeacherSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://search.gmw.cn/search.do?cp=1&q={0}".format(keyword)]
        self.index = 1

    def get_next_url(self, OldUrl):
        l = OldUrl.split('=')
        p = re.compile(r'[0-9]+')
        OldID = int(p.match(l[1]).group())
        NewID = OldID + 1
        NewUrl = l[0] + '=' + str(NewID) + '&q=' + l[2]
        return str(NewUrl)

    def parse(self, response):
        is_ha = False
        for sel in response.xpath('//ul[@class="media-list"]/li'):
            try:
                if sel:
                    is_ha = True
                    item = SearchListItem()
                    item['title'] = sel.xpath('div/h4/a//text()').extract()
                    item['url'] = sel.xpath('div/h4/a/@href').extract()
                    item['abstract'] = [''.join(sel.xpath('div/p//text()').extract()).replace('\n', '').replace('\u3000', '').replace(' ', '')]
                    item['imgs'] = sel.xpath('div/a/img/@src').extract()
                    content =sel.xpath('div/h4/span/text()').extract()[0].split(' ')
                    item['media_name'] = [content[0]]
                    item['published_at'] = [content[1]+' '+content[2]]
                    item['index'] = self.index
                    self.index += 1
                    # 发布时间控制
                    if int(content[1].replace('-', '')) < self.dt:
                        return
                    yield item
            except:
                print("error")
        if is_ha:
            next_Url = self.get_next_url(response.url)
            yield scrapy.Request(next_Url, callback=self.parse, dont_filter=True)
        else:
            return

