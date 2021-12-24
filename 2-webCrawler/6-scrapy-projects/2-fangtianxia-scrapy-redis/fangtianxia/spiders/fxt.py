import scrapy
from scrapy_redis.spiders import RedisSpider

from ..items import FangtianxiaItem


class FxtSpider(RedisSpider):
    name = 'fxt'
    allowed_domains = ['fang.com']
    # start_urls = ['http://fang.com/']
    redis_key = 'fang:url'  # 数据库列表名， 通过redis数据库向爬虫框架分发任务

    def parse(self, response):
        tr_eles = response.css('#c02 tr')

        province = None
        for tr_ele in tr_eles:
            pro = tr_ele.css('td[valign="top"] strong::text').get()
            if pro:
                if pro.strip():
                    province = pro
            if province == '其他':
                continue
            cities = tr_ele.css('td a')
            for city in cities:
                city_name = city.css('::text').get()
                city_url = city.css('::attr(href)').get()
                yield scrapy.Request(city_url,
                                     callback=self.parse_city_url,
                                     meta={'province': province, 'city_name': city_name})

    def parse_city_url(self, response):
        """过度函数， 知识用来解析新房地址， 解析到新房地址， 我们继续进入获取到相关详细信息。"""
        new_house_url = response.css('#dsy_D01_02 div.s4Box a::attr(href)').get()
        if new_house_url:
            yield scrapy.Request(new_house_url,
                                 callback=self.parse_house_details,
                                 meta=response.request.meta)

    def parse_house_details(self, response):
        province = response.request.meta.get('province')
        city_name = response.request.meta.get('city_name')

        # parse details
        li_eles = response.css('.nl_con.clearfix>ul>li')
        for li_ele in li_eles:
            name = li_ele.css('.nlcd_name a::text').get().strip()
            price = li_ele.css('.nhouse_price span::text').get()  # some price is hidden in the i tag
            if not price:
                price = li_ele.css('.nhouse_price i::text').get()

            house_type = li_ele.css('.house_type  a::text').getall()
            house_area = li_ele.css('.house_type::text').re('[\d~平米]+')
            in_sale = li_ele.css('.fangyuan span::text').get().strip()
            details_url = li_ele.css(' .nlcd_name a::attr(href)').get()

            yield FangtianxiaItem(province=province,
                                  city_name=city_name,
                                  name=name,
                                  price=price,
                                  house_type=house_type,
                                  house_area=house_area,
                                  sale=in_sale,
                                  details_url=details_url)

            # next page
