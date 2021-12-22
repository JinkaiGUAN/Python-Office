# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

from itemadapter import ItemAdapter


class FangtianxiaPipeline:

    def __init__(self):
        self.filename = './fangtianxia.csv'
        self.file = open(self.filename, mode='a', encoding='utf-8', newline='')
        self.csv_writer = csv.DictWriter(self.file, fieldnames=['province', 'city_name', 'name', 'price', 'house_type',
                                                                'house_area', 'sale', 'details_url'])
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        self.csv_writer.writerow(dict(item))
        return item

    def close_spider(self, spider):
        self.file.close()
