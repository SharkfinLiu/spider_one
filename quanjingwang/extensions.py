from collections import defaultdict

from scrapy.extensions import closespider
from scrapy import signals
from scrapy.exceptions import NotConfigured


class CloseSpiderByRule(closespider.CloseSpider):
    """
    在setting中设定以下值指定停止条件：
    CLOSESPIDER_TIMEOUT：等待时间
    CLOSESPIDER_ITEMCOUNT：抓取item数
    CLOSESPIDER_PAGECOUNT：抓取页数
    CLOSESPIDER_ERRORCOUNT：遇到的错误
    CLOSESPIDER_URL：遇到的指定URL
    """
    def __init__(self, crawler):
        self.crawler = crawler

        self.close_on = {
            'timeout': crawler.settings.getfloat('CLOSESPIDER_TIMEOUT'),
            'itemcount': crawler.settings.getint('CLOSESPIDER_ITEMCOUNT'),
            'pagecount': crawler.settings.getint('CLOSESPIDER_PAGECOUNT'),
            'errorcount': crawler.settings.getint('CLOSESPIDER_ERRORCOUNT'),
            "meeturl": crawler.settings.get('CLOSESPIDER_URL'),
            "itemurl": crawler.settings.get('CLOSESPIDER_ITMURL')
            }

        if not any(self.close_on.values()):
            raise NotConfigured

        self.counter = defaultdict(int)

        if self.close_on.get('errorcount'):
            crawler.signals.connect(self.error_count, signal=signals.spider_error)
        if self.close_on.get('pagecount'):
            crawler.signals.connect(self.page_count, signal=signals.response_received)
        if self.close_on.get('timeout'):
            crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
        if self.close_on.get('itemcount'):
            crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
        if self.close_on.get('meeturl'):
            crawler.signals.connect(self.request_meet, signal=signals.request_scheduled)
        if self.close_on.get('itemurl'):
            crawler.signals.connect(self.item_meet, signal=signals.item_scraped)     # TODO
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    def request_meet(self, request, spider):
        if request.url == self.close_on['meeturl']:
            self.crawler.engine.close_spider(spider, 'closespider_meeturl')

    def item_meet(self, item, spider):
        if item.get("url") == self.close_on["itemurl"]:
            self.crawler.engine.close_spider(spider, 'closespider_itemurl')