# -*- coding: UTF-8 -*-
"""
@Project : 2-GameInfoCrawler 
@File    : get_single_game_info.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 31/08/2021 07:51 
@Brief   : 
"""
import csv
import random
import time
import os

import requests
import parsel


class GetSingleGameInfo:
    MY_USER_AGENT = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]

    My_PROXIES = [
        'http://163.125.222.76:8118','http://117.94.222.121:3256',
        'http://183.47.237.251:80','http://60.185.203.76:3000',
        'http://140.255.139.161:3256','http://123.171.42.181:3256',
        'http://129.226.182.125:80','http://106.45.104.214:3256',
        'http://110.87.176.121:8118','http://183.47.237.251:80',
        'http://115.209.75.14:3000','http://111.225.153.120:3256',
        'http://117.94.222.93:3256','http://47.75.132.50:8118',
        'http://123.171.42.218:3256','http://121.232.148.3:3256',
        'http://121.232.148.78:3256','http://123.171.42.85:3256',
        'http://106.45.105.221:3256', 'http://183.47.237.251:80'
    ]
    def __init__(self, game_name = None, game_index = None):
        self.game_name = game_name
        self.game_index = game_index  # this is the index corresponding to the game

        # search page
        self.url = 'https://www.vgtime.com/search/game.jhtml'
        self.headers = {
            "Host": "www.vgtime.com",
            "Referer": "https://www.vgtime.com/search/list.jhtml?keyword=.hack//G.U.Last%20Recode",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        self.data_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'original'))
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)

        # self.proxies = {
        #     "http": "http://121.230.210.218:3256", "http": "http://121.226.21.79:3256",
        #     "http": "http://117.65.1.30:3256", "http": "http://47.98.179.39:8080",
        #     "http": "http://182.87.138.104:3256", "http": "http://117.64.237.234:1133",
        #     "http": "http://60.167.134.98:1133", "http": "http://220.179.219.174:1133",
        # }

        # detail page
        self.headers_detail = {
            "referer": "https://www.vgtime.com/search/list.jhtml?keyword=.hack//G.U.Last%20Recode", # key word需要根据游戏名进行更换
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }

    def get_params(self, game_name: str = '.hack//G.U.Last Recode', page_num: int = 1):
        """This will return the query parameters when searching."""
        return {
            'keyword': game_name,
            'type': 'game',
            'page': str(page_num),
            'pageSize': '12',
            'domName': 'search_game_list',
        }

    def update_headers(self):
        self.headers['user-agent'] = random.choice(self.MY_USER_AGENT)

    def update_headers_detail(self):
        self.headers['user-agent'] = random.choice(self.MY_USER_AGENT)

    def get_response(self, url: str, page_num: int = 1):
        response = requests.get(url, headers=self.update_headers(), params=self.get_params(page_num=page_num),
                                timeout=10, proxies={'http': random.choice(self.My_PROXIES)})
        time.sleep(2)
        return response

    def get_total_page_num(self, url):
        response = self.get_response(url)
        selector = parsel.Selector(response.text)
        total_data = selector.css('body a.load_more::attr(data-total)').get()
        page_num = int(total_data) // 12 + 1
        return page_num

    def parse_single_page(self, url, page_num: int = 1):
        # url is not changed, but the parameters do
        response = self.get_response(url, page_num=page_num)
        selector = parsel.Selector(response.text)
        li_eles = selector.css('body li')
        data_list = []
        for li_ele in li_eles:
            img_url = li_ele.css('a:nth-child(1) img::attr(src)').get()
            detail_page_url = 'https://www.vgtime.com' + li_ele.css('div.info_box a::attr(href)').get()
            data_list.append((img_url, detail_page_url))

        return data_list

    def save_data_for_games_list(self, data_list):
        with open(os.path.join(self.data_path, '1.csv'), mode='a', encoding='utf-8', newline='\n') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data_list)

    def parse_detail_page(self, url):
        response = requests.get(url, headers=self.update_headers_detail(), timeout=10,
                                proxies={'http': random.choice(self.My_PROXIES)})
        time.sleep(2)
        selector = parsel.Selector(response.text)
        chinese_name = selector.css('div.game_box.main:nth-child(1) h2 a::text').get()
        english_name = selector.css('div.game_box.main:nth-child(1) p::text').get()
        english_name = chinese_name if english_name == '' else english_name

        # 发行时间
        release_time_list = []
        try:
            releases = selector.css('div.game_descri div.descri_box.plat_date_detail')
            for release in releases[:-1]:  # size -> 2
                release_time_list.append(release.css('span:nth-child(1)::text').get())
        except:
            release_time_list = [selector.css('div.game_descri div.descri_box:nth-child(2) span::text').text()]

        # release_time = selector.css('div.game_descri div.descri_box:nth-child(2) span::text').text()

        # platform  # 带有悬浮窗口的页面
        platforms = selector.css('div.game_descri div:nth-child(1) div span')
        platform_list = []
        for platform in platforms: # size -> 2
            platform_name = platform.css('::text').get()
            # 是否支持中文
            try:
                # chinese_version_support_tag = 'Yes' if platform.css('::attr(data-cn)').get() else 'No'
                chinese_version_support_tag = platform.css('::attr(data-cn)').get()
            except Exception as e:
                chinese_version_support_tag = 'false'

            platform_list.append((platform_name, chinese_version_support_tag))

        # 可能带有链接
        try:
            developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) span::text').get()
        except:
            developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) a::text').get()

        try:
            publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) span::text').get()
        except:
            publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) a::text').get()


        # developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) span::text').get()
        # publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) span::text').get()

        # 无悬浮窗
        # platforms = selector.css('div.game_descri div:nth-child(1) div span')
        # for platform in platforms:
        #     plat_form_name = platform.css('::text').get()

        print(chinese_name, english_name, release_time_list, platform_list, developer, publisher)

    def run(self):
        total_page_num = self.get_total_page_num(self.url)

        for page_num in range(total_page_num + 1):
            data_list = self.parse_single_page(self.url, page_num)
            for _, detail_url in data_list:
                self.parse_single_page(detail_url, )
            # self.save_data_for_games_list(data_list)
            print('<--------------- Page {} saved! --------------->'.format(page_num))
            break

if __name__ == "__main__":
    get_single_game = GetSingleGameInfo()
    get_single_game.run()
