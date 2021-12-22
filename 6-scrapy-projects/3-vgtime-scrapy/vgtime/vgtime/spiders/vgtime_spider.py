import copy
import os.path
import time

import scrapy
from ..items import VgtimeItem
import pandas as pd
from urllib.parse import quote


class VgtimeSpiderSpider(scrapy.Spider):
    name = 'vgtime_spider'
    allowed_domains = ['vgtime.com']

    def start_requests(self):
        # data = pd.read_csv(os.path.abspath(os.path.join(os.getcwd(), '..', 'input_files', 'GameNameList.csv')))[:1]
        # game_names = data['GameName']
        game_names = [ '幻想高尔夫', '428 被封锁的涩谷', '1001颗钉子', '百尺机器人高尔夫']
        print('Game Names: ', game_names)

        for game_name in game_names:
            url = f'http://www.vgtime.com/search/game.jhtml?keyword={quote(game_name)}&type=game&page=1&pageSize=12&domName=search_game_list'
            yield scrapy.Request(url, callback=self.parse, meta={'GameName': game_name})

    def parse(self, response):
        game_name = response.meta.get('GameName')
        game_nums = response.css('body a.load_more::attr(data-total)').get()
        # 此处需考虑特殊情况， 即 num可能位0 但是实际上还是有数据的情况， 此时页数就为1
        if not game_nums:
            game_nums = response.css('body span::attr(data-total)').get()

        if int(game_nums) < 1 or game_nums is None:
            page_num = 1
        else:
            page_num = int(game_nums) // 12 + 1

        if not response.meta.get('CurrentPageNum'):
            current_page = 1
        else:
            current_page = response.meta.get('CurrentPageNum')

        # get the image url, the url to the detail pages
        li_eles = response.css('body li')
        for li_ele in li_eles:
            img_url = li_ele.css('.img_box a img::attr(src)').get()
            detail_url = 'http://www.vgtime.com' + li_ele.css('.img_box a::attr(href)').get()
            # 链接到下一个解析函数， 但是headers得变换， 应该说是refere核host要变， 变为当前页面的url
            # Referer: http://www.vgtime.com/search/game.jhtml?keyword=%E6%80%AA%E7%89%A9%E7%8C%8E%E4%BA%BA&type=game&page=1&pageSize=12&domName=search_game_list
            yield scrapy.Request(detail_url, callback=self.parse_details,
                                 meta={'detailsReferer': response.request.url, 'img_url': img_url, 'GameName': game_name})

        # 实现翻页
        if current_page < page_num:
            current_page += 1
            url = f'http://www.vgtime.com/search/game.jhtml?keyword={quote(game_name)}&type=game&page={current_page}&pageSize=12&domName=search_game_list'
            yield scrapy.Request(url, callback=self.parse,
                                 meta={'CurrentPageNum': current_page, 'GameName': game_name})

    def parse_details(self, response):
        game_name = response.meta.get('GameName')
        img_url = response.meta.get('img_url')
        # time.sleep(np.random.rand() + 1)
        chinese_name = response.css('div.game_box.main:nth-child(1) h2 a::text').get()
        english_name = response.css('div.game_box.main:nth-child(1) p::text').get()
        english_name = chinese_name if english_name is None else english_name

        # 发行时间。 暂时还未发现在一张详情页里， 有的标签可以浮动显示， 有的不可以
        release_time_list = []
        # 1. 这是能出现浮动页面的发行时间
        releases = response.css('div.game_descri div.descri_box.plat_date_detail')
        if releases:
            for release in releases[:-1]:  # 此处我们已经省略了最开始出现在界面中的时间
                release_time_list.append(release.css('span:nth-child(1)::text').get())
        # 2. 这是没有浮动界面的发行时间，此时只有一个元素。
        if not release_time_list:
            release_time_list = [response.css('.game_descri .descri_box:nth-child(2) span::text').get()]

        # platform  # 带有悬浮窗口的页面
        platforms = response.css('div.game_descri div:nth-child(1) div span')
        platform_list = []
        for platform in platforms:  # size -> 2
            platform_name = platform.css('::text').get()
            # 是否支持中文
            chinese_version_support_tag = platform.css('::attr(data-cn)').get()
            chinese_version_support_tag = 'false' if chinese_version_support_tag is None else 'true'

            platform_list.append((platform_name, chinese_version_support_tag))

        # 开发者 发行者, 此处是因为存在中不同的样式， 其中有的开发者核发行者可能带有链接
        developer = response.css('div.game_descri div.descri_box:nth-last-child(2) span::text').get()
        if developer is None:
            developer = response.css('div.game_descri div.descri_box:nth-last-child(2) a::text').get()

        publisher = response.css('div.game_descri div.descri_box:nth-last-child(1) span::text').get()
        if publisher is None:
            publisher = response.css('div.game_descri div.descri_box:nth-last-child(1) a::text').get()

        # data processing
        # brand_list = [('pc', 'ChineseVersion1'), ('ps4', 'ChineseVersion2'), ('ps5', 'ChineseVersion3'),
        #               ('xbox one', 'ChineseVersion4'), ('xbox serious', 'ChineseVersion5'),
        #               ('switch', 'ChineseVersion6'), ('3ds', 'ChineseVersion7'), ('psv', 'ChineseVersion8')]

        brand_list_new_version = [('pc', 'ChineseVersion1'), ('ps4', 'ChineseVersion2'), ('ps5', 'ChineseVersion3'),
                                  ('xb1', 'ChineseVersion4'), ('xsx|s', 'ChineseVersion5'),
                                  ('ns', 'ChineseVersion6'), ('3ds', 'ChineseVersion7'), ('psv', 'ChineseVersion8')]

        data = {'ChineseName': game_name, 'GameName': chinese_name, 'EnglishName': english_name,
                'Developer': developer, 'Publisher': publisher}

        release_time_list = [release_time_list[0] for _ in range(len(platform_list))] if len(
            release_time_list) <= 1 else release_time_list

        platform_string = ''
        for (platform_true, chinese_version_true), release_time in zip(platform_list, release_time_list):

            if '最早发售' in release_time:
                release_time = release_time.replace('\xa0', " ").split(" ")[1]
            elif '(' in release_time:
                release_time = release_time.split('(')[0]

            platform_string = platform_string + platform_true.lower() + ', '
            # for brand, chinese_version in brand_list:
            for brand, chinese_version in brand_list_new_version:
                if platform_true.lower() == brand:
                    data[copy.deepcopy(brand)] = copy.deepcopy(release_time)
                    data[copy.deepcopy(chinese_version)] = copy.deepcopy(chinese_version_true)

            # for brand, chinese_version in brand_list:
            for brand, chinese_version in brand_list_new_version:
                if brand not in data.keys():
                    data[copy.deepcopy(brand)] = ''
                    data[copy.deepcopy(chinese_version)] = ''

        data['SupportPlatforms'] = platform_string
        yield VgtimeItem(
            ChineseName=data.get('ChineseName'),
            GameName=data.get('GameName'),
            EnglishName=data.get('EnglishName'),
            SupportPlatforms=data.get('SupportPlatforms'),
            Developer=data.get('Developer'),
            Publisher=data.get('Publisher'),
            pc=data.get('pc'),
            ChineseVersion1=data.get('ChineseVersion1'),
            ps4=data.get('ps4'),
            ChineseVersion2=data.get('ChineseVersion2'),
            ps5=data.get('ps5'),
            ChineseVersion3=data.get('ChineseVersion3'),
            xbox_one=data.get('xb1'),
            ChineseVersion4=data.get('ChineseVersion4'),
            xbox_serious=data.get('xsx|s'),
            ChineseVersion5=data.get('ChineseVersion5'),
            switch=data.get('ns'),
            ChineseVersion6=data.get('ChineseVersion6'),
            three_ds=data.get('3ds'),
            ChineseVersion7=data.get('ChineseVersion7'),
            psv=data.get('psv'),
            ChineseVersion8=data.get('ChineseVersion8'),
            ImgUrl=img_url
        )
