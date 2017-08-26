import json
import codecs



class JsonWithEncodingquanjingwangPipeline(object):
    def __init__(self):
        self.file = codecs.open('qjw.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=True) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class Scrapy_gmw_dataPipeline(object):
    def __init__(self):
        self.file = codecs.open('gmw.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=True) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()