# -*- coding: utf-8 -*-
import scrapy
import re
import time
from quanjingwang.items import SearchListItem


class P5wSearchSpider(scrapy.Spider):
    count = 1  # index
    dt = 20130816  # 发布时间
    name = 'p5w_P5wSearchSpider'
    allowed_domains = ['http://www.p5w.net/']
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "ct.p5w.net",
        "Origin": "http://www.p5w.net",
        "Referer": "http://www.p5w.net/so/index.html?keyword=%E5%B0%8F%E7%B1%B3",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
    }

    def __init__(self, keyword=None, *args, **kwargs):
        super(P5wSearchSpider, self).__init__(*args, **kwargs)
        cur = (time.time()) * 1000
        self.start_urls = ["http://ct.p5w.net/api/sh/sh/article?keyword=%s&page=1&size=10&_=%s" % (keyword, cur)]

    def get_next_url(self, oldUrl):
        cur = (time.time()) * 1000
        l = oldUrl.split('=')
        p = re.compile(r'[0-9]+')
        oldID = int(p.match(l[2]).group())
        newID = oldID + 1
        newUrl = l[0] + '=' + l[1] + '=' + str(newID) + '&size=' + l[3] + str(int(cur))
        return str(newUrl)

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse, headers=self.headers)

    def parse(self, response):
        is_ha = False
        for sel in response.xpath('//div[@class="searchlist"]/ul/li'):
            try:
                if sel:
                    is_ha = True
                    item = SearchListItem()
                    item['title'] = sel.xpath('h3/a//text()').extract()
                    item['url'] = sel.xpath('h3/a/@href').extract()
                    # url限制
                    # if item['url'][0] == 'http://www.p5w.net/kuaixun/201406/t20140617_640323.htm':
                    #     return
                    item['abstract'] = sel.xpath('p/text()').extract()
                    # item['media_name'] = sel.xpath('span/a/text()').extract()
                    item['published_at'] = sel.xpath('span/text()').extract()
                    str_convert = ''.join(item['published_at']).replace('\n', '').strip()
                    # item['published_at'] = scrapy.Field()
                    item['published_at'] = [str_convert]
                    # print(item['published_at'])
                    it = str_convert.split(' ')
                    it = it[0].replace('-', '')
                    # 时间控制
                    if int(it) < self.dt:
                        return
                    item['index'] = self.count
                    self.count += 1
                    # print(self.count)
                    yield item
            except:
                print("error")
        if is_ha:
            next_Url = self.get_next_url(response.url)
            yield scrapy.Request(next_Url, callback=self.parse, headers=self.headers, dont_filter=True)
        else:
            return
