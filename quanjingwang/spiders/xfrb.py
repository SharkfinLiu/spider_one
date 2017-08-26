# -*- coding: utf-8 -*-
import scrapy
import re
from quanjingwang.items import SearchListItem

class XfrbSearchSpider(scrapy.Spider):
    name = 'xfrb_XfrbSearchSpider'
    allowed_domains = ['www.xfrb.com']
    # dt = 20170331  # 发布时间

    def __init__(self, keyword=None, *args, **kwargs):
        super(XfrbSearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://user.xfrb.com.cn/index.php/Search/index/keywords/{0}/p/1.html".format(keyword)]
        self.index = 1

    def get_next_url(self, Oldurl):
        l = Oldurl.split('/')
        p = re.compile(r'[0-9]+')
        OldID = int(p.match(l[-1]).group())
        NewId = OldID + 1
        NewUrl = l[0] + '//' + l[2] + '/' + l[3] + '/' + l[4] + '/' + l[5] + '/' + l[6] + '/' + l[7] + '/' + l[8] + '/' + str(NewId) + '.html'
        return str(NewUrl)

    def parse(self, response):
        is_ha = False
        for sel in response.xpath('//div[@class="list_box"]'):
            for sel1 in sel.xpath('a'):
                if sel:
                    is_ha = True
                    item = SearchListItem()
                    item['url'] = sel1.xpath('@href').extract()
                    item['title'] = [''.join(sel1.xpath('div/div[@class="list_text"]/h3//text()').extract())]
                    item['published_at'] = sel1.xpath('div/div[@class="list_text"]/h4/text()').extract()
                    item['index'] = self.index
                    self.index += 1
                    # split_publish_at = item['published_at'][0].replace('-', '')
                    # 发布时间控制
                    # if int(split_publish_at) < self.dt:
                    #     return
                    yield item
        if is_ha:
            next_Url = self.get_next_url(response.url)
            yield scrapy.Request(next_Url, callback=self.parse, dont_filter=True)
        else:
            return
