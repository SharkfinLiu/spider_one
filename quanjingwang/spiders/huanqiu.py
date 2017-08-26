# -*- coding: utf-8 -*-
import scrapy
from quanjingwang.items import SearchListItem
import scrapy_splash


class HuanqiuSearchSpider(scrapy.Spider):
    name = 'huanqiu_HuanqiuSearchSpider'
    allowed_domains = ['s.huanqiu.com/']
    # start_urls = ["http://s.huanqiu.com/s/?q=小米&p=1"]
    # headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    #            "Accept-Encoding": "gzip, deflate",
    #            "Accept-Language": "en-US,en;q=0.5",
    #            "Cache-Control": "max-age=0",
    #            "Connection": "keep-alive",
    #            "Host": "s.huanqiu.com",
    #            "Upgrade-Insecure-Requests": "1",
    #            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0"}
    # cookies = {
    #     "Hm_lvt_1fc983b4c305d209e7e05d96e713939f": "1503548405",
    #     "Hm_lpvt_1fc983b4c305d209e7e05d96e713939f": "1503567470",
    #     "UM_distinctid": "15e1277f89d9-0c3fdeb3c9703b8-75246751-1fa400-15e1277f89f80",
    #     "_ma_tk": "16t6bfycge6jgh9ijqf8e74a9jezl2at",
    #     "_ma_is_new_u": "1",
    #     "_ma_starttm": "1503548422744",
    #     "CNZZDATA1000010102": "2104743357-1503546934-http%253A%252F%252Fwww.huanqiu.com%252F%7C1503563134",
    #     "HQ-ANTI-BOT": "647017005cb8f94fd256a4848103c29357f8a3d2"
    # }

    def __init__(self, keyword=None, *args, **kwargs):
        super(HuanqiuSearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://s.huanqiu.com/s/?q={0}&p=1".format(keyword)]
        self.index = 1

    # def get_next_url(self, OldUrl):
    #     l = OldUrl.split('=')
    #     OldID = int(l[2])
    #     NewID = OldID + 1
    #     NewUrl = l[0] + '=' + l[1] + '=' + str(NewID)
    #     return str(NewUrl)

    def start_requests(self):
        # yield scrapy.Request(self.start_urls[0], callback=self.parse, headers=self.headers, cookies=self.cookies)
        yield scrapy_splash.SplashRequest(self.start_urls, callback=self.parse, args={'wait': 0.5})

    def parse(self, response):
        # is_ha = False
        # # sel = response.xpath('//div[@class="sList"]')
        return

        # try:
        #     if sel:
        #         is_ha = True
        #         item = SearchSpiderItem()
        #         item['title'] = sel.xpath('dl/dd/h3/a//text()')
        #         item['url'] = sel.xpath('dl/dd/h3/a/@href')
        #         item['abstract'] = sel.xpath('dl/dd/p//text()')
        #         content = sel.xpath('dl/dd/span/text()')
        #         yield item
        # except:
        #     print("error")


"""


"""