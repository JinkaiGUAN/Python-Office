# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Jobs51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    SearchName = scrapy.Field()
    JobName = scrapy.Field()
    CompanyName = scrapy.Field()
    WorkingArea = scrapy.Field()
    Salary = scrapy.Field()
