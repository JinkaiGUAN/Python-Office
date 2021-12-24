# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VgtimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ChineseName = scrapy.Field()
    GameName = scrapy.Field()
    EnglishName = scrapy.Field()
    SupportPlatforms = scrapy.Field()
    Developer = scrapy.Field()
    Publisher = scrapy.Field()
    pc = scrapy.Field()
    ChineseVersion1 = scrapy.Field()
    ps4 = scrapy.Field()
    ChineseVersion2 = scrapy.Field()
    ps5 = scrapy.Field()
    ChineseVersion3 = scrapy.Field()
    xbox_one = scrapy.Field()
    ChineseVersion4 = scrapy.Field()
    xbox_serious = scrapy.Field()
    ChineseVersion5 = scrapy.Field()
    switch = scrapy.Field()
    ChineseVersion6 = scrapy.Field()
    three_ds = scrapy.Field()
    ChineseVersion7 = scrapy.Field()
    psv = scrapy.Field()
    ChineseVersion8 = scrapy.Field()
    ImgUrl = scrapy.Field()
