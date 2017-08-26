# -*- coding: utf-8 -*-
import scrapy
from quanjingwang.items import SearchListItem
import scrapy.cmdline
import requests
import json
import codecs


class GuanchaSearchSpider(scrapy.Spider):
    count = 1  # index
    dt = 20130601  # 发布时间
    name = 'guancha_GuanchaSearchSpider'
    allowed_domains = ['http://www.guancha.cn']

    def __init__(self, keyword=None, *args, **kwargs):
        super(GuanchaSearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.guancha.cn/Search/?k=%s&y=1&ps=20&pi=1' % keyword]

    def get_next_url(self, oldUrl):
        l = oldUrl.split('=')
        oldID = int(l[4])
        newID = oldID + 1
        newUrl = l[0] + '=' + l[1] + '=' + l[2] + '=' + l[3] + '=' + str(newID)
        return str(newUrl)

    def start_requests(self):
        # headers = test_spider.headers_s()
        yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        # print('2222222')
        is_ha = False
        for sel in response.xpath('//dl[@class="search-list"]/dd'):
            try:
                if sel:
                    is_ha = True
                    item = SearchListItem()
                    item['title'] = sel.xpath('h4/a/text()').extract()
                    item['url'] = sel.xpath('h4/a/@href').extract()
                    item['url'][0] = 'http://www.guancha.cn' + item['url'][0]
                    # url限制
                    # if item['url'][0] == 'http://www.guancha.cn/TMT/2017_08_03_421220.shtml':
                    #     return
                    item['abstract'] = sel.xpath('p/text()').extract()
                    # item['browse_num'] = sel.xpath('div/a[@class="interact-attention"]/text()').extract()
                    # item['answer'] = sel.xpath('div/a[@class="interact-comment"]/text()').extract()
                    item['published_at'] = sel.xpath('div/span/text()').extract()
                    str_convert = ''.join(item['published_at']).replace('\n', '').strip()
                    item['published_at'] = [str_convert]
                    it = str_convert.split(' ')
                    it = it[0].replace('-', '')
                    # 时间控制
                    if int(it) < self.dt:
                        return
                    item['index'] = self.count
                    self.count += 1
                    yield item
                    # 写出数据
                    self.p_item(item)
            except:
                print("error")
        if is_ha:
            next_Url = self.get_next_url(response.url)
            yield scrapy.Request(next_Url, callback=self.parse, dont_filter=True)
        else:
            return

    def p_item(self, item):
        f = codecs.open('observer.json', 'a', encoding='utf-8')
        line = json.dumps(dict(item), ensure_ascii=True) + "\n"
        f.write(line)
        f.close()
