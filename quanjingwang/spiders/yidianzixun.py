
# -*- coding: utf-8 -*-
import re
import urllib.parse

import requests
from pz.tools.unit import clean_stylescriptother
from scrapy.spiders import CrawlSpider
from starcloudlib.pzlog.logger import *

from scrapy_sina.items import *
from scrapy_sina.settings import LOGPATH,MAIN_DIR
from scrapy_sina.utils.util import peek


class YidianzixunListSpider(scrapy.Spider):
    name = "yidianzixun_YidianzixunListSpider"
    allowed_domains = ["yidianzixun.com"]
    custom_settings = {
        # "DEFAULT_REQUEST_HEADERS": SEARCH_HEADERS,
        # "LOG_FILE": LOGPATH+name+".log",
        # "LOG_FILE": os.getcwd()+"/sina_list.log",
        "ITEM_PIPELINES": {
            'scrapy_sina.pipelines.ScrapySinaFilePipeline': 300,
        },
        "output_file": MAIN_DIR + "/data/" + name
    }
    query = {
        "display": "",
        "cstart": 0,
        "cend": 10,
        "word_type": "token",
        "multi": 5,
        "appid": "web_yidian"
    }
    template = "http://www.yidianzixun.com/home/q/news_list_for_keyword?"

    def __init__(self, keyword, *args, **kwargs):
        super(YidianzixunListSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'http://www.yidianzixun.com/home/q/news_list_for_keyword?display=%s&cstart=0&cend=10&word_type=token&multi=5&appid=web_yidian&_=1496281535324' % keyword]
        self.keyword = urllib.parse.unquote(keyword)

        self._logger = logger(LOGPATH + self.name + ".log").getLogger()
        self._logger.info("-----------------%s start!-------------------" % self.name)

    def parse(self, response):
        raw = json.loads(response.body_as_unicode())
        entries = raw.get("result", {})
        if not entries or raw.get("status")!='success':
            self._logger.info("not a good response for request:%s, maybe reached the end!" % response.url)
            return
        for entry in entries:
            if not entry.get("title"):
                continue
            yield from self.fill_item(entry)

        self.query['cstart'] = self.query["cend"]
        self.query['cend'] = self.query["cend"] + 10
        self.query['display'] = self.keyword
        # total_page = int(int(raw["result"]['count'])/int(self.query['num'])) + 1
        # if self.query['page'] > 3:

        next_page = self.template + urllib.parse.urlencode(self.query)
        yield scrapy.Request(next_page, callback=self.parse)

    def fill_item(self, entry):
        result_data = ListItem()
        result_data["title"] = entry.get("title", "")
        result_data["url"] = "http://www.yidianzixun.com/article/" + entry.get("itemid", "")
        result_data["media_name"] = entry.get("source", "")
        result_data["create_at"] = entry.get("date", "")
        result_data["channel"] = entry.get("category", "")
        yield result_data


class YidianzixunSearchSpider(YidianzixunListSpider):
    name = "yidianzixun_YidianzixunSearchSpider"
    custom_settings = {
        # "DEFAULT_REQUEST_HEADERS": SEARCH_HEADERS,
        # "LOG_FILE": LOGPATH+name+".log",
        # "LOG_FILE": os.getcwd()+"/sina_list.log",
        "ITEM_PIPELINES": {
            'scrapy_sina.pipelines.ScrapySinaFilePipeline': 300,
        },
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_sina.middlewares.ProxyMiddleware': 100,
            # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 107,
        },
        "output_file": MAIN_DIR + "/data/" + name
    }

    def __init__(self, keyword, *args, **kwargs):
        super(YidianzixunSearchSpider, self).__init__(keyword, *args, **kwargs)
        self.index = 1

    def fill_item(self, entry):
        result_data = SearchListItem()
        result_data["title"] = entry.get("title", "")
        result_data["url"] = "http://www.yidianzixun.com/article/" + entry.get("itemid", "")
        result_data["media_name"] = entry.get("source", "")
        result_data["published_at"] = entry.get("date", "")
        result_data["channel"] = entry.get("category", "")
        result_data["abstract"] = entry.get("summary", "")
        result_data["index"] = self.index
        result_data["imgs"] = ["http://i1.go2yd.com/image.php?type=thumbnail_336x216&url=" + entry.get("image")] if entry.get("image") else []

        self.index += 1
        yield result_data



class YidianzixunArtSpider(CrawlSpider):
    name = "yidianzixun_YidianzixunArtSpider"
    allowed_domains = ["yidianzixun.com"]
    start_urls = []
    custom_settings = {
        "ITEM_PIPELINES": {
            'scrapy_sina.pipelines.ScrapyTemFilePipeline': 300,
        },
        "output_file": name
    }
    url_match = r'^http[s]?://www.yidianzixun.com/article/.+?$'

    def __init__(self, url, *args, **kwargs):
        super(YidianzixunArtSpider, self).__init__(*args, **kwargs)
        self._logger = logger(LOGPATH + self.name + ".log").getLogger()
        if re.match(self.url_match, url):
            self.start_urls = [url]
        else:
            self._logger.info("get unmatch url: %s" % url)
        self._logger.info("-----------------YidianzixunArt start!-------------------")

    def parse_start_url(self, response):
        contents_list = response.xpath("//div[@class='content-bd']/p | //div[@id='imedia-article']/p").extract()

        content = ""
        if len(contents_list) > 0:
            content = ''.join(contents_list)

        span_pub_list = response.xpath("//div[@class='meta']/span/text()").extract()

        publish_at_str = ''
        for sp_itm in span_pub_list:
            if re.match("^[\d]",sp_itm):
                publish_at_str = sp_itm
                break

        if isinstance(publish_at_str,(list,set)):
            publish_at_str = publish_at_str[0] if len(publish_at_str) > 0 else ""

        # get author
        ref_media_sel = response.xpath("//div[@class='meta']/a")

        if not ref_media_sel:
            ref_media_sel = response.xpath("//div[@class='doc-channel-wrapper']/a[2]")

        ref_author = ref_media_sel.xpath("text()").extract()

        origin_url_elem = peek(response.xpath("//div[@class='meta']/span/text()").extract())

        page_data = YidianzixunArtItem()
        page_data["title"] = peek(response.xpath("//h2/text()").extract())
        page_data["author"] = peek(ref_author) #response.css("span.media_name").extract()
        page_data["origin_media_name"] = "" if not origin_url_elem.startswith("来源") else peek(origin_url_elem.split("："), -1)
        page_data["origin_url"] = "" if not origin_url_elem.startswith("来源") else ""
        page_data["content"] = clean_stylescriptother(content)
        page_data["publish_at"] = publish_at_str
        page_data["tags"] = []
        page_data["result_tags"] = "_bud_self" if response.xpath("//div[@class='meta']/span[@class='wm-copyright']") else "_bud_reship"
        imgs = response.css("span.a-image img")
        page_data["imgs"] = [peek(img.xpath("@src").extract()) for img in imgs]
        page_data["url"] = response.url
        page_data["slug"] = ""
        page_data["read_num"] = ""
        page_data["like_num"] = ""
        page_data["dislike_num"] = ""
        page_data["comment_num"] = ""
        page_data["encode"] = response.encoding
        page_data["all"] = ""
        page_data["kw"] = ""
        page_data["murl"] = "http://www.yidianzixun.com"+peek(ref_media_sel.xpath("@href").extract()) if ref_media_sel else ""

        page_data["minfo"] = {
            "platform": {
            "avater": "http://star.static.puzhizhuhai.com/img/0303.png",
            "platform_url": "http://www.yidianzixun.com",
            "mid": "yidianzixun.com",
            "name": "一点资讯"
            },
            "code": peek(page_data["murl"].split("/"), -1),
            "circulation_medium":"网站",
            "avater": peek(response.xpath("//div[@class='wemedia-wrapper']/a/img/@src | //div[@class='doc-channel-wrapper']/a/img/@src").extract()),
            "name": page_data["author"],
            "url": page_data["murl"],
            "certification": {
                "property": "",
                "name": "",
                "all_record": "",
                "record": "",
                "owner": ""
            }
        }
        yield page_data


class YidianzixunMedSpider(CrawlSpider):
    name = "yidianzixun_YidianzixunMedSpider"
    allowed_domains = ["yidianzixun.com"]
    start_urls = []
    custom_settings = {
        "ITEM_PIPELINES": {
            'scrapy_sina.pipelines.ScrapyTemFilePipeline': 300,
        },
        "output_file": name
    }
    url_match = r'^http[s]?://www.yidianzixun.com/channel/.+?$'

    def __init__(self, url, *args, **kwargs):
        super(YidianzixunMedSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self._logger = logger(LOGPATH+self.name+".log").getLogger()
        self._logger.info("-----------------YidianzixunMedia start!-------------------")

    def parse_start_url(self, response):
        page_data = YidianzixunMedItem()
        page_data["code"] = peek(response.url.split("/"), -1)
        page_data["platform"] = {
            "avater": "http://star.static.puzhizhuhai.com/img/0303.png",
            "platform_url": "http://www.yidianzixun.com",
            "mid": "yidianzixun.com",
            "name": "一点资讯"
        }
        page_data["rank"] = 0
        page_data["url"] = response.url
        page_data["is_auth"] = False
        page_data["auth_level"] = ""

        q = {                                                   #具体信息需要ajax
            "channel_id": page_data["code"],
            "cstart": "0",
            "cend": "10",
            "infinite": "true",
            "refresh": "1",
            "multi": "5",
            "appid": "web_yidian",
            # "_": "1495617770469",
        }
        r = requests.get("http://www.yidianzixun.com/home/q/news_list_for_channel", q)
        data = json.loads(r.content.decode())
        page_data["avater"] = data.get("channel_image")#peek(response.xpath('//img[@class="channel-image"]/@src').extract())
        page_data["desc"] = data.get("channel_summary")#peek(response.xpath("//p[@class='channel-summary']/text()").extract())              #TODO
        page_data["name"] = data.get("channel_name")#peek(response.xpath("//p[@class='channel-name']/text()").extract())
        fans = data.get("bookcount")#response.xpath("//p[class='channel-bookcount']")
        if fans:
            # fans = peek(fans.xpath("text()").re("\d+"))
            fans = re.search("[\d.]+", fans)
            fans = float(fans.group())*10000 if fans else ""
        page_data["fans_num"] = fans if fans else ""
        page_data["follow_num"] = ""
        page_data["certification"] = {
               "property":"",
               "name":"",
               "all_record":"",
               "record":"",
               "owner":""
              }
        yield page_data