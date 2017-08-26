# -*- coding: utf-8 -*-
import scrapy
import re
from quanjingwang.items import SearchListItem
import traceback

class ChinasoSearchSpider(scrapy.Spider):
    name = 'chinaso_ChinasoSearchSpider'
    allowed_domains = ['www.chinaso.com']
    # iii = 1

    def __init__(self, keyword=None, *args, **kwargs):
        super(ChinasoSearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.chinaso.com/search/pagesearch.htm?q={0}&page=1&wd={0}".format(keyword)]
        self.index = 1

    def get_next_url(self, OldUrl):
        l = OldUrl.split('=')
        p = re.compile(r'[0-9]+')
        OldID = int(p.match(l[2]).group())
        NewId = OldID + 1
        NewUrl = l[0] + '=' + l[1] + '=' + str(NewId) + '&wd=' + l[3]
        return str(NewUrl)

    def parse(self, response):
        # is_ha =False
        for sel in response.css('.reItem '):
            if sel.xpath('h2'):
                item = SearchListItem()
                item['title'] = ''.join(sel.xpath('h2/a//text()').extract())
                item['url'] = sel.xpath('h2/a/@href').extract()
                item['url'] = ''.join(["http://www.chinaso.com"] + item['url'])
                item['imgs'] = sel.xpath('div[@class="reNewsWrapper clearfix"]/div[@class="reNewsImgWrapper fl"]/div[@class="imgVM"]/a/span/img/@src').extract()
                item['abstract'] = ''.join(sel.xpath('div[@class="reNewsWrapper clearfix"]/div[@class="reNewsContL fr"]/p[1]//text()').extract()).replace('\n', '').replace(' ', '')
                content = sel.xpath('div[@class="reNewsWrapper clearfix"]/div[@class="reNewsContL fr"]/p[@class="snapshot"]/span/text()').extract()
                # print(content)
                if content:
                    p_published_at = re.compile(r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)')
                    if p_published_at.search(content[0]):
                        item['published_at'] = [p_published_at.search(content[0]).group()]
                    p_media = re.compile(r'(\S*)*(\s-\s)*(https://)*(\w*\.)*(\w*)')
                    media_content = p_media.match(content[0]).group().split('-')
                    item['media_name'] = media_content[0].strip()
                    if len(media_content) > 1:
                        item['media_url'] = media_content[1].strip()
                item['index'] = self.index
                self.index += 1
                yield item
        # is_ha = response.xpath('//div[@id="pager"]/a[@_dom_name="next"]')
        # if is_ha:
        #     next_Url = self.get_next_url(response.url)
        #     yield scrapy.Request(next_Url, callback=self.parse, dont_filter=True)
        # else:
        return

