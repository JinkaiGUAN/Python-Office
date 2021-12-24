# -*- coding: UTF-8 -*-
"""
@Project : 2-GameInfoCrawler 
@File    : test_latin.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 31/08/2021 16:37 
@Brief   : 
"""
import csv
import random
import threading
import time
import os

import copy
import requests
import parsel
import numpy as np
import concurrent.futures


class GetSingleGameInfo:
    MY_USER_AGENT = [
        # "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        # "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        # "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        # "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        # "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        # "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        # "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        # """
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
"Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36",
"Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19",
"Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZ054K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
"Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
    ]

    My_PROXIES = [
        # 'http://163.125.222.76:8118','http://117.94.222.121:3256',
        # 'http://183.47.237.251:80','http://60.185.203.76:3000',
        # 'http://140.255.139.161:3256','http://123.171.42.181:3256',
        # 'http://129.226.182.125:80','http://106.45.104.214:3256',
        # 'http://110.87.176.121:8118','http://183.47.237.251:80',
        # 'http://115.209.75.14:3000','http://111.225.153.120:3256',
        # 'http://117.94.222.93:3256','http://47.75.132.50:8118',
        # 'http://123.171.42.218:3256','http://121.232.148.3:3256',
        # 'http://121.232.148.78:3256','http://123.171.42.85:3256',
        # 'http://106.45.105.221:3256', 'http://183.47.237.251:80'

        # 'http://106.45.104.216:3256','http://117.94.222.225:3256',
        # 'http://59.55.162.72:3256','http://112.195.243.238:3256',
        # 'http://101.200.127.149:3129','http://111.77.112.64:3256',
        # 'http://39.105.156.161:8118','http://121.232.148.167:3256',
        # 'http://112.195.242.172:3256','http://39.103.175.42:3128',
        # 'http://101.200.127.149:3129','http://101.200.127.149:3129',
        # 'http://182.84.145.121:3256','http://121.230.210.232:3256',
        # 'http://111.72.25.180:3256','http://182.84.145.100:3256',
        # 'http://101.200.127.149:3129','http://101.200.127.149:3129','http://121.226.21.38:3256',
        # 'http://121.230.210.9:3256', 'http://121.232.148.216:3256' ,
        
# 'http://112.195.241.247:3256','http://183.47.237.251:80','http://47.75.132.50:8118','http://182.84.145.23:3256','http://112.195.240.49:3256','http://223.244.179.74:3256','http://117.69.230.199:3256','http://115.218.4.236:9000','http://27.191.60.86:3256','http://117.94.222.80:3256',

'http://123.171.42.85:3256','http://163.125.29.74:8118','http://182.84.145.167:3256','http://106.45.104.208:3256','http://117.35.255.154:3000','http://1.83.116.200:8118','http://1.83.116.200:8118','http://111.225.153.182:3256','http://106.45.104.52:3256','http://163.125.222.223:8118','http://27.191.60.58:3256','http://47.104.15.198:80',
    ]

    def __init__(self, game_name = None, game_index = None):
        self.game_name = game_name
        self.game_index = game_index  # this is the index corresponding to the game
        self.lock = threading.Lock()

        # search page
        self.url = 'https://www.vgtime.com/search/game.jhtml'
        self.headers = {
            'Host': 'www.vgtime.com',
            "Referer": "https://www.vgtime.com/search/list.jhtml",
            # "Referer": "https://www.vgtime.com/search/list.jhtml?keyword={}".format(self.game_name),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        self.data_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'original'))
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
        self.url_data_path = os.path.join(self.data_path, str(self.game_index) + '.csv')
        self.original_data_path = os.path.join(self.data_path, str(self.game_index) + '-details.csv')
        self.clear_data_in_csv()
        self.log_path = './log.txt'

        # detail page
        self.headers_detail = {
            # "referer": "https://www.vgtime.com/search/list.jhtml?keyword=.hack//G.U.Last%20Recode", # key word需要根据游戏名进行更换
            "referer": "https://www.vgtime.com/search/list.jhtml?keyword={}".format(self.game_name),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }

    def clear_data_in_csv(self):
        with open(self.url_data_path, 'a+', encoding='utf-8-sig') as test:
            test.truncate(0)
        with open(self.original_data_path, 'a+', encoding='utf-8-sig') as test:
            test.truncate(0)

        self.keys = [
                'GameName','EnglishName',
                    'SupportPlatforms','Developer','Publisher','pc','ChineseVersion1',
                    'ps4','ChineseVersion2','ps5','ChineseVersion3','xbox one','ChineseVersion4',
                    'xbox serious','ChineseVersion5','switch','ChineseVersion6','3ds',
                    'ChineseVersion7','psv','ChineseVersion8'
                ]
        with open(self.original_data_path, mode='a', encoding='utf-8-sig', newline='\n') as f:
            csv_writer = csv.DictWriter(f, fieldnames=self.keys)
            csv_writer.writeheader()

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
        response = self.get_response(url)  # 返回response.url
        self.headers_detail['referer'] = response.url
        selector = parsel.Selector(response.text)
        total_data = selector.css('body a.load_more::attr(data-total)').get()
        if not total_data and (response.status_code < 400):
            page_num = 1
        else:
            page_num = int(total_data) // 12 + 1
        return page_num

    def parse_single_page(self, url, page_num: int = 1, times : int = 5):
        try:
            # url is not changed, but the parameters do
            response = self.get_response(url, page_num=page_num)

            if response.status_code > 400:
                if times >= 1:
                    self.parse_single_page(url, page_num, times - 1)
                else:
                    raise Exception("Game: \t" + str(self.game_index) + " " + self.game_name + " " + str(response.status_code))
                self.lock.acquire()
                with open(self.log_path, mode='a', encoding='utf-8', newline='\n') as f:
                    f.write("Time: \t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                    f.write("Game: \t" + str(self.game_index) + " " + self.game_name + " " + str(response.status_code))
                    f.write('\n')
                self.lock.release()

            else:
                selector = parsel.Selector(response.text)
                li_eles = selector.css('body li')
                data_list = []
                for li_ele in li_eles:
                    img_url = li_ele.css('a:nth-child(1) img::attr(src)').get()
                    detail_page_url = 'https://www.vgtime.com' + li_ele.css('div.info_box a::attr(href)').get()
                    data_list.append((img_url, detail_page_url))

                return data_list

        except Exception as e:
            if times >= 1:
                self.parse_single_page(url, page_num, times - 1)
            self.lock.acquire()
            with open(self.log_path, mode='a', encoding='utf-8', newline='\n') as f:
                f.write("Time: \t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                f.write("Game: \t" + str(self.game_index) + " " + self.game_name + " " + str(response.status_code))
                f.write(str(e))
                f.write('\n')
            self.lock.release()

            print(e)

    def save_data_for_games_list(self, data_list):
        self.lock.acquire()
        with open(self.url_data_path, mode='a', encoding='utf-8-sig', newline='\n') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data_list)
        self.lock.release()

    def __get_response_for_detail__(self, url, times: int = 5):
        response = requests.get(url, headers=self.headers_detail, timeout=10,
                                proxies={'http': random.choice(self.My_PROXIES)})

        if response.status_code > 350:
            if times >= 1:
                response = self.__get_response_for_detail__(url, times - 1)
            else:
                self.lock.acquire()
                with open(self.log_path, mode='a', encoding='utf-8', newline='\n') as f:
                    f.write("Time: \t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
                    f.write("Game: \t" + str(self.game_index) + " " + self.game_name + " " + str(response.status_code))
                    f.write('\n')
                self.lock.release()

                return None

        return response

    def parse_detail_page(self, url, times: int = 5):
        print(url)
        response = self.__get_response_for_detail__(url, times)

        time.sleep(np.random.rand() + 1)
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

        # data processing
        brand_list = [('pc', 'ChineseVersion1'),
                      ('ps4', 'ChineseVersion2'), ('ps5', 'ChineseVersion3'), ('xbox one', 'ChineseVersion4'),
                      ('xbox serious', 'ChineseVersion5'), ('switch', 'ChineseVersion6'), ('3ds',
                        'ChineseVersion7'), ('psv', 'ChineseVersion8')]

        data = {'GameName': chinese_name, 'EnglishName': english_name, 'Developer': developer, 'Publisher': publisher}

        # release_time_list = release_time_list if len(release_time_list) <= 1 else release_time_list[:-1]
        release_time_list = [release_time_list[0] for _ in range(len(platform_list))] if len(
            release_time_list) <= 1 else release_time_list[:-1]

        # print(release_time_list)

        platform_string = ''

        for (platform_true, chinese_version_true), release_time in zip(platform_list, release_time_list):

            platform_string = platform_string + platform_true.lower() + ', '
            for brand, chinese_version in brand_list:
                if platform_true.lower() == brand:
                    data[copy.deepcopy(brand)] = copy.deepcopy(release_time)
                    data[copy.deepcopy(chinese_version)] = copy.deepcopy(chinese_version_true)

            for brand, chinese_version in brand_list:
                if brand not in data.keys():
                    data[copy.deepcopy(brand)] = ''
                    data[copy.deepcopy(chinese_version)] = ''

        data['SupportPlatforms'] = platform_string

        # print(data)
        return data

    def save_data_for_details(self, data_dict_list):
        self.lock.acquire()
        with open(self.original_data_path, mode='a', encoding='utf-8-sig', newline='\n') as f:
            if len(data_dict_list) > 0:
                csv_writer = csv.DictWriter(f, fieldnames=self.keys)
                # csv_writer.writeheader()
                csv_writer.writerows(data_dict_list)
            print(data_dict_list)
        self.lock.release()

    def run(self):
        total_page_num = self.get_total_page_num(self.url)
        # #
        for page_num in range(1, total_page_num + 1):
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
        # time.sleep(10)

    def __run__(self, page_num):
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

    def main_thread(self):
        total_page_num = self.get_total_page_num(self.url)
        print("Total page number is: ", total_page_num)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for page_num in range(1, total_page_num + 1):
                executor.submit(self.__run__, page_num)

    def __main_thread__(self, page_num):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.submit(self.__run__, page_num)

    def main_process(self):
        total_page_num = self.get_total_page_num(self.url)
        print("Total page number is: ", total_page_num)

        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
            for page_num in range(1, total_page_num + 1):
                executor.submit(self.__main_thread__, page_num)

if __name__ == "__main__":
    time_start = time.time()
    name = '.hack//G.U.Last Recode' #'NBA 2K17'
    index = 1 #163

    # 帝国时代3 终极版 60
    # index = 111 愤怒的小鸟：星球大战 offset = 110
    # index = 160 NB                offset = 159
    # index = 162 NBA 2K15          offset = 161
    # 163 NBA 2K17
    try:
        get_single_game = GetSingleGameInfo(game_name=name, game_index=index)
        # get_single_game.run()
        # get_single_game.main_thread()
        get_single_game.main_process()
    except Exception as e:
        print("Time used: ", time.time() - time_start)
        raise e

