# -*- coding:utf-8 -*-
from scrapy.crawler import CrawlerProcess
from quanjingwang.spiders.p5w import P5wSearchSpider
from quanjingwang.spiders.guancha import GuanchaSearchSpider
from quanjingwang.spiders.ob import ObSpider
from quanjingwang.spiders.chinaso import  ChinasoSearchSpider
from quanjingwang.spiders.chinanews import ChinanewsSearchSpider
from quanjingwang.spiders.xfrb import XfrbSearchSpider
from quanjingwang.spiders.huanqiu import HuanqiuSearchSpider
from quanjingwang.spiders.gmw import GmwSeacherSpider

p = CrawlerProcess({})
p.crawl(HuanqiuSearchSpider, "小米")
p.start()
