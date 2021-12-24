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
import threading
import time
import os

import requests
import parsel
import numpy as np
import concurrent.futures


class GetSingleGameInfo:
    MY_USER_AGENT = [
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
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
        self.lock = threading.Lock()

        # search page
        self.url = 'https://www.vgtime.com/search/game.jhtml'
        self.headers = {
            'Host': 'www.vgtime.com',
            # "Referer": "https://www.vgtime.com/search/list.jhtml?keyword=.hack//G.U.Last%20Recode",
            "Referer": "https://www.vgtime.com/search/list.jhtml?keyword={}".format(self.game_name),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        self.data_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'original'))
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
        self.url_data_path = os.path.join(self.data_path, str(self.game_index) + '.csv')
        self.original_data_path = os.path.join(self.data_path, str(self.game_index) + '-details.csv')
        self.clear_data_in_csv()

        # detail page
        self.headers_detail = {
            # "referer": "https://www.vgtime.com/search/list.jhtml?keyword=.hack//G.U.Last%20Recode", # key word需要根据游戏名进行更换
            "referer": "https://www.vgtime.com/search/list.jhtml?keyword={}".format(self.game_name),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }

    def clear_data_in_csv(self):
        with open(self.url_data_path, 'a+', encoding='utf-8') as test:
            test.truncate(0)
        with open(self.original_data_path, 'a+', encoding='utf-8') as test:
            test.truncate(0)

        print('<----------- Clear data in CSV files! ------------>')

    def get_params(self, game_name: str = '.hack//G.U.Last Recode', page_num: int = 1):
        """This will return the query parameters when searching."""
        return {
            'keyword': self.game_name,
            'type': 'game',
            'page': str(page_num),
            'pageSize': '12',
            'domName': 'search_game_list',
        }

    def update_headers(self):
        self.headers['User-Agent'] = random.choice(self.MY_USER_AGENT)

    def update_headers_detail(self):
        self.headers['user-agent'] = random.choice(self.MY_USER_AGENT)

    def get_response(self, url: str, page_num: int = 1):
        # response = requests.get(url, headers=self.update_headers(), params=self.get_params(page_num=page_num),
                                # timeout=10, proxies={'http': random.choice(self.My_PROXIES)})
        response = requests.get(url, headers=self.headers, params=self.get_params(page_num=page_num),
                                timeout=10, proxies={'http': random.choice(self.My_PROXIES)})
        time.sleep(2 * np.random.rand() + 1)
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
        self.lock.acquire()
        with open(os.path.join(self.data_path, str(self.game_index) + '.csv'), mode='a', encoding='utf-8', newline='\n') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data_list)
        self.lock.release()

    def parse_detail_page(self, url):
        print(url)
        response = requests.get(url, headers=self.headers_detail, timeout=10,
                                proxies={'http': random.choice(self.My_PROXIES)})
        time.sleep(2 * np.random.rand() + 1)
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
            if release_time_list == []:
                release_time_list = [selector.css('div.game_descri div.descri_box:nth-child(2) span::text').get()]
        except:
            release_time_list = [selector.css('div.game_descri div.descri_box:nth-child(2) span::text').get()]

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
                if chinese_version_support_tag == None:
                    chinese_version_support_tag = 'false'
            except Exception as e:
                chinese_version_support_tag = 'false'

            platform_list.append((platform_name, chinese_version_support_tag))

        # 可能带有链接
        try:
            developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) span::text').get()
            if developer == None:
                developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) a::text').get()
        except:
            developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) a::text').get()

        try:
            publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) span::text').get()
            if publisher == None:
                publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) a::text').get()
        except:
            publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) a::text').get()

        data = {"ChineseName": chinese_name, "EnglishName": english_name, "ReleaseTimeList": release_time_list,
         "PlatformList": platform_list, "Developer": developer, "Publisher": publisher, "DetailUrl": url}
        print(data)
        return data

    def save_data_for_details(self, data_dict_list):
        self.lock.acquire()
        with open(os.path.join(self.data_path, str(self.game_index) + '-details.csv'), mode='a', encoding='utf-8', newline='\n') as f:
            csv_writer = csv.DictWriter(f, fieldnames=data_dict_list[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data_dict_list)
        self.lock.release()

    def run(self, page_num):
        # total_page_num = self.get_total_page_num(self.url)
        #
        # for page_num in range(1, total_page_num + 1):
        print('<--------------- Page {} is parsing! --------------->'.format(page_num))
        data_list = self.parse_single_page(self.url, page_num)
        # print(data_list)
        self.save_data_for_games_list(data_list)

        data_dict_list = []
        for _, detail_url in data_list:
            time.sleep(2 * np.random.rand() + 1)
            data_dict_list.append(self.parse_detail_page(detail_url))

        self.save_data_for_details(data_dict_list)

        print('<--------------- Page {} saved! --------------->'.format(page_num))
        # break
        time.sleep(10)

    def main_thread(self):
        total_page_num = self.get_total_page_num(self.url)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for page_num in range(1, total_page_num + 1):
                executor.submit(self.run, page_num)


if __name__ == "__main__":
    time_start = time.time()
    try:
        get_single_game = GetSingleGameInfo(game_name='.hack//G.U.Last Recode', game_index=1)
        # get_single_game.run()
        get_single_game.main_thread()
    except Exception as e:
        print("Time used: ", time.time() - time_start)
        raise e



#     params = {
#         'keyword': '.hack//G.U.Last Recode',
#         'type': 'game',
#         'page': '1',
#         'pageSize': '12',
#         'domName': 'search_game_list',
#     }
#     url = 'http://www.vgtime.com/search/game.jhtml'
#     headers = {
# 'Host': 'www.vgtime.com',
# 'Referer': 'https://www.vgtime.com/search/list.jhtml?keyword=.hack//G.U.%20Last%20Recode',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
#     }
#     response = requests.get(url, params=params, headers=headers)
#
#     selector = parsel.Selector(response.text)
#     total_data = selector.css('body a.load_more::attr(data-total)').get()
#     page_num = int(total_data) // 12 + 1
#     print(page_num)