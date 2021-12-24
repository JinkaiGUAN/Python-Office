# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os.path

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class VgtimePipeline:
    def process_item(self, item, spider):
        return item


class CsvPipeline:

    def __init__(self):
        self.file = open('./vgtime.csv', mode='a', encoding='utf-8', newline='')
        self.csv_writer = csv.DictWriter(self.file, fieldnames=[
            'ChineseName', 'GameName', 'EnglishName', 'SupportPlatforms', 'Developer', 'Publisher', 'pc',
            'ChineseVersion1', 'ps4', 'ChineseVersion2', 'ps5', 'ChineseVersion3', 'xbox_one',
            'ChineseVersion4', 'xbox_serious', 'ChineseVersion5', 'switch', 'ChineseVersion6',
            'three_ds', 'ChineseVersion7', 'psv', 'ChineseVersion8', 'ImgUrl',
        ])
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        self.csv_writer.writerow(dict(item))
        return item

    def close_spider(self, spider):
        self.file.close()


from .settings import IMAGES_STORE


class ImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        img_url = item['ImgUrl']

        yield scrapy.Request(img_url, meta={'FolderName': item['ChineseName'], 'HeadersCheck': 'No'})

    def file_path(self, request, response=None, info=None, *, item=None):
        dir_name = request.meta.get('FolderName')
        # "https://img01.vgtime.com/game/web/150429235337830.jpg?x-oss-process=image/resize,w_300"
        img_name = request.url.split('?')[0].split('/')[-1]
        print('Image Name ----->, ', os.path.abspath(os.path.join(IMAGES_STORE, dir_name, img_name)))

        # return os.path.join(dir_name, img_name)
        return dir_name + '\\' + img_name
