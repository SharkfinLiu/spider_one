# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    media_name = scrapy.Field()  # 媒体名
    title = scrapy.Field()  # 若为页面搜索爬虫则为处理后标题
    url = scrapy.Field()  # 项目链接
    published_at = scrapy.Field()  # 项目创建时间
    imgs = scrapy.Field()  # 图片链接数组
    channel = scrapy.Field()  # 频道
    media_url = scrapy.Field()  # 媒体url
    abstract = scrapy.Field()  # 简介
    index = scrapy.Field()  # 排名
    original_title = scrapy.Field()  # 页面搜索爬虫专有, 原始标题
