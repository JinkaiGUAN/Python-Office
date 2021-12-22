# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtianxiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    house_type = scrapy.Field()
    house_area = scrapy.Field()
    sale = scrapy.Field()
    details_url = scrapy.Field()  # 强青叶url地址
