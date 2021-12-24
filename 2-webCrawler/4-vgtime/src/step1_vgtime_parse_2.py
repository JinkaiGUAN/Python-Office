# -*- coding: UTF-8 -*-
"""
@Project : 4-vgtime 
@File    : step1_vgtime_parse_2.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 02/09/2021 17:47 
@Brief   : 
"""

import csv
import random
import threading
import time
import os
import pandas as pd

import copy
import requests
import parsel
import numpy as np
import concurrent.futures


class GetSingleGameInfo:
    MY_USER_AGENT = [
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
        # 'http://112.195.241.247:3256','http://183.47.237.251:80','http://47.75.132.50:8118','http://182.84.145.23:3256','http://112.195.240.49:3256','http://223.244.179.74:3256','http://117.69.230.199:3256','http://115.218.4.236:9000','http://27.191.60.86:3256','http://117.94.222.80:3256',

        'http://123.171.42.85:3256', 'http://163.125.29.74:8118', 'http://182.84.145.167:3256',
        'http://106.45.104.208:3256', 'http://117.35.255.154:3000', 'http://1.83.116.200:8118',
        'http://1.83.116.200:8118', 'http://111.225.153.182:3256', 'http://106.45.104.52:3256',
        'http://163.125.222.223:8118', 'http://27.191.60.58:3256', 'http://47.104.15.198:80',
    ]

    def __init__(self, game_name=None, game_index=None, log_folder=None):
        self.game_name = game_name
        self.game_index = game_index  # this is the index corresponding to the game
        self.lock = threading.Lock()

        # search page
        self.url = 'https://www.vgtime.com/search/game.jhtml'
        self.headers = {
            'Host': 'www.vgtime.com',
            "Referer": "https://www.vgtime.com/search/list.jhtml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        # The path where crawler stores
        data_folder = os.path.abspath(os.path.join(os.getcwd(), '..', 'data'))
        # The folder stores all images we need
        self.image_folder = os.path.join(data_folder, 'Images')
        if not os.path.exists(self.image_folder):
            os.mkdir(self.image_folder)

        # The file stores the first game information when we search in the engine
        self.first_game_info_csv_path = os.path.join(data_folder, 'first_game_info.csv')
        # The file stores all details we need written in the docs.
        self.final_detail_csv_path = os.path.join(data_folder, 'final_details.csv')
        self.config_csv_file()

        self.log_path = os.path.join(log_folder, 'log.txt')

        # detail page
        self.headers_detail = {
            "referer": "https://www.vgtime.com/search/list.jhtml?keyword={}".format(self.game_name),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }

    def config_csv_file(self):
        self.image_csv_keys = ['InputGameName', 'ActualGameName', 'ImageURL', 'DetailPageURL']
        self.details_keys = [
            'ChineseName', 'GameName', 'EnglishName',
            'SupportPlatforms', 'Developer', 'Publisher', 'pc', 'ChineseVersion1',
            'ps4', 'ChineseVersion2', 'ps5', 'ChineseVersion3', 'xbox one', 'ChineseVersion4',
            'xbox serious', 'ChineseVersion5', 'switch', 'ChineseVersion6', '3ds',
            'ChineseVersion7', 'psv', 'ChineseVersion8'
        ]
        self.details_keys_new_version = [
            'ChineseName', 'GameName', 'EnglishName',
            'SupportPlatforms', 'Developer', 'Publisher', 'pc', 'ChineseVersion1',
            'ps4', 'ChineseVersion2', 'ps5', 'ChineseVersion3', 'xb1', 'ChineseVersion4',
            'xsx|s', 'ChineseVersion5', 'ns', 'ChineseVersion6', '3ds',
            'ChineseVersion7', 'psv', 'ChineseVersion8'
        ]

        if self.game_index == 1:
            print('<----------- Configure Headers in CSV File! ------------>')
            with open(self.first_game_info_csv_path, mode='a', encoding='utf-8-sig', newline='\n') as f:
                f.truncate(0)
                csv_writer = csv.DictWriter(f, fieldnames=self.image_csv_keys)
                csv_writer.writeheader()

            with open(self.final_detail_csv_path, mode='a', encoding='utf-8-sig', newline='\n') as f:
                f.truncate(0)
                csv_writer = csv.DictWriter(f, fieldnames=self.details_keys)
                # csv_writer = csv.DictWriter(f, fieldnames=self.details_keys_new_version)
                csv_writer.writeheader()

    def get_params(self, page_num: int = 1):
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

    def get_response(self, url: str, page_num: int = 1, times: int = 5):
        response = requests.get(url, headers=self.headers, params=self.get_params(page_num=page_num),
                                timeout=10, proxies={'http': random.choice(self.My_PROXIES)})

        if response.status_code > 400:
            if times >= 1:
                self.get_response(url, page_num=1, times=times - 1)
            else:
                self.write_log(str(response.status_code))
                return None
        else:
            return response

    def __get_response_for_detail__(self, url, times: int = 5):
        response = requests.get(url, headers=self.headers_detail, timeout=10,
                                proxies={'http': random.choice(self.My_PROXIES)})

        if response.status_code > 350:
            if times >= 1:
                response = self.__get_response_for_detail__(url, times - 1)
            else:
                self.write_log(str(response.status_code))
                return None

        return response

    def parse_detail_page(self, url, times: int = 5):
        # print(url)
        response = self.__get_response_for_detail__(url, times)

        if not response:
            self.write_log('Response is None for detail page')
            return self.return_none_detail()
        else:

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
            for platform in platforms:  # size -> 2
                platform_name = platform.css('::text').get()
                # 是否支持中文
                try:
                    # chinese_version_support_tag = 'Yes' if platform.css('::attr(data-cn)').get() else 'No'
                    chinese_version_support_tag = platform.css('::attr(data-cn)').get()
                    if chinese_version_support_tag is None:
                        chinese_version_support_tag = 'false'
                except Exception as e:
                    chinese_version_support_tag = 'false'

                platform_list.append((platform_name, chinese_version_support_tag))

            # 可能带有链接
            try:
                developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) span::text').get()
                if developer is None:
                    developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) a::text').get()
            except:
                developer = selector.css('div.game_descri div.descri_box:nth-last-child(2) a::text').get()

            try:
                publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) span::text').get()
                if publisher is None:
                    publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) a::text').get()
            except:
                publisher = selector.css('div.game_descri div.descri_box:nth-last-child(1) a::text').get()

            # data processing
            brand_list = [('pc', 'ChineseVersion1'), ('ps4', 'ChineseVersion2'), ('ps5', 'ChineseVersion3'),
                          ('xbox one', 'ChineseVersion4'), ('xbox serious', 'ChineseVersion5'),
                          ('switch', 'ChineseVersion6'), ('3ds', 'ChineseVersion7'), ('psv', 'ChineseVersion8')]

            brand_list_new_version = [('pc', 'ChineseVersion1'), ('ps4', 'ChineseVersion2'), ('ps5', 'ChineseVersion3'),
                                      ('xb1', 'ChineseVersion4'), ('xsx|s', 'ChineseVersion5'),
                                      ('ns', 'ChineseVersion6'), ('3ds', 'ChineseVersion7'), ('psv', 'ChineseVersion8')]

            data = {'ChineseName': self.game_name, 'GameName': chinese_name, 'EnglishName': english_name,
                    'Developer': developer, 'Publisher': publisher}

            # release_time_list = release_time_list if len(release_time_list) <= 1 else release_time_list[:-1]
            try:
                release_time_list = [release_time_list[0] for _ in range(len(platform_list))] if len(
                    release_time_list) <= 1 else release_time_list
            except:
                release_time_list = [release_time_list[0] for _ in range(len(platform_list))] if len(
                    release_time_list) <= 1 else release_time_list[:-1]
            # print(release_time_list)

            platform_string = ''

            # print(len(platform_list), len(release_time_list))
            for (platform_true, chinese_version_true), release_time in zip(platform_list, release_time_list):

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

            # print(data)
            return data

    def get_first_game_basic_info(self, url: str):
        """This function will grasp the image url and detail page url for the first game."""
        response = self.get_response(url,
                                     page_num=1)  # parse the first page, however, we need to note that the response could be 403.
        time.sleep(np.random.rand() + 1)
        self.headers_detail['referer'] = response.url
        selector = parsel.Selector(response.text)
        try:
            game_num = int(selector.css('body a.load_more::attr(data-total)').get())
        except:
            game_num = int(selector.css('body span::attr(data-total)').get())

        if game_num < 1:
            return game_num, {
                'InputGameName': self.game_name, 'ActualGameName': None, 'ImageURL': None,
                'DetailPageURL': None}
        else:
            first_li_ele = selector.css('body li.game:nth-child(1)')
            game_name = first_li_ele.css('div.info_box h2 a::text').get()
            image_url = first_li_ele.css('div.img_box a img::attr(src)').get()
            detail_page_url = 'https://www.vgtime.com' + first_li_ele.css('div.info_box h2 a::attr(href)').get()

            return game_num, {
                'InputGameName': self.game_name, 'ActualGameName': game_name, 'ImageURL': image_url,
                'DetailPageURL': detail_page_url}

    def save_image_data(self, data_dict):
        image_url = data_dict['ImageURL']
        postfix = image_url.split('?')[0].split('.')[-1]
        image_name = str(self.game_index) + '.' + postfix
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }
        data = requests.get(image_url, headers=headers, timeout=10).content
        with open(os.path.join(self.image_folder, image_name), mode='wb') as f:
            f.write(data)
        self.lock.acquire()
        with open(self.first_game_info_csv_path, mode='a', encoding='utf-8-sig', newline='\n') as f:
            csv_writer = csv.DictWriter(f, fieldnames=self.image_csv_keys)
            csv_writer.writerow(data_dict)
        self.lock.release()

    def save_detail_page_info(self, detail_dict):
        self.lock.acquire()
        with open(self.final_detail_csv_path, mode='a', encoding='utf-8-sig', newline='\n') as f:
            # csv_writer = csv.DictWriter(f, fieldnames=self.details_keys)
            csv_writer = csv.DictWriter(f, fieldnames=self.details_keys_new_version)
            csv_writer.writerow(detail_dict)
        self.lock.release()

    def write_log(self, info: str):
        self.lock.acquire()
        with open(self.log_path, mode='a', encoding='utf-8', newline='\n') as f:
            f.write("Time: \t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + '\t')
            f.write("ErrorInfo: \tindex = " + str(
                self.game_index) + " real name = " + self.game_name + '\t' + "Reason = " + info)
            f.write('\n')
        self.lock.release()

    def return_none_detail(self):
        # return {'ChineseName': self.game_name, 'GameName': self.game_name, 'EnglishName': None,
        #         'SupportPlatforms': None, 'Developer': None, 'Publisher': None, 'pc': None, 'ChineseVersion1': None,
        #         'ps4': None, 'ChineseVersion2': None, 'ps5': None, 'ChineseVersion3': None, 'xbox one': None,
        #         'ChineseVersion4': None,
        #         'xbox serious': None, 'ChineseVersion5': None, 'switch': None, 'ChineseVersion6': None, '3ds': None,
        #         'ChineseVersion7': None, 'psv': None, 'ChineseVersion8': None}
        return {'ChineseName': self.game_name, 'GameName': self.game_name, 'EnglishName': None,
                'SupportPlatforms': None, 'Developer': None, 'Publisher': None, 'pc': None, 'ChineseVersion1': None,
                'ps4': None, 'ChineseVersion2': None, 'ps5': None, 'ChineseVersion3': None, 'xb1': None,
                'ChineseVersion4': None,
                'xsx|s': None, 'ChineseVersion5': None, 'ns': None, 'ChineseVersion6': None, '3ds': None,
                'ChineseVersion7': None, 'psv': None, 'ChineseVersion8': None}

    def run(self):
        # 1. Get the image url, name and detail page url for the first page.
        print('<--------------- Fist Game of Index={} GameName={} Is Parsing! --------------->'.format(self.game_index,
                                                                                                       self.game_name))
        game_num, image_dict = self.get_first_game_basic_info(self.url)
        # 2. Save information and the image.
        # print(image_dict)
        self.save_image_data(image_dict)
        if game_num < 1:
            print('No Game!')
            self.write_log("No Game")
            detail_dict = self.return_none_detail()
            self.save_detail_page_info(detail_dict)
        else:
            # 3. Parse detail page
            detail_dict = self.parse_detail_page(image_dict['DetailPageURL'])
            # if detail_dict == None:
            #     pass
            # else:
            # 5. Save detail page information
            self.save_detail_page_info(detail_dict)
            print('<--------------- Data Saved for Index={} GameName={}! --------------->'.format(self.game_name,
                                                                                                  self.game_index))


def main_thread(offset, game_name_data, log_folder):
    """
    offset : 1000
    game_name_data : [1000, 2000]
    index = 1001
    """
    for index, game_name in enumerate(game_name_data):
        if (index + 1 + offset) % 500 == 0 and offset != 0:
            print("<--------------------- Pause the Machine --------------------->")
            print("Time: \t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            time.sleep(150)

        print(index + 1 + offset, game_name, )
        time_start = time.time()
        try:
            get_single_game = GetSingleGameInfo(game_name=game_name, game_index=index + 1 + offset,
                                                log_folder=log_folder)
            get_single_game.run()
            print("Time used: ", time.time() - time_start)
        except Exception as e:
            print("Time used: ", time.time() - time_start)
            print(e)


def create_log_folder():
    base_log = os.path.abspath(os.path.join(os.getcwd(), '..', 'log'))
    if not os.path.exists(base_log):
        os.mkdir(base_log)

    folder_path = os.path.join(base_log, time.strftime("%Y-%m-%d", time.localtime(time.time())))
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    return folder_path


def main_process():
    """Since we use multiprocess for this programme, the order of the game is not so sequential, however, we
    use the original chinese name as the index to instruct us."""
    log_folder_path = create_log_folder()

    game_list_data = pd.read_csv(os.path.abspath(os.path.join(os.getcwd(), '..', 'input_files', 'NewGameList.csv')))

    # game_name_data = game_list_data.loc[:, 'GameName'][offset:50]
    offsets = [0, 1000, 2000, 3000]
    game_name_lists = [game_list_data.loc[:, 'GameName'][offsets[0]:offsets[1]],
                       game_list_data.loc[:, 'GameName'][offsets[1]:offsets[2]],
                       game_list_data.loc[:, 'GameName'][offsets[2]:offsets[3]],
                       game_list_data.loc[:, 'GameName'][offsets[3]:]]
    # print(game_name_list)
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for offset, game_name_list in zip(offsets, game_name_lists):
            executor.submit(main_thread, offset, game_name_list, log_folder_path)


if __name__ == "__main__":
    main_process()

    # game_name = '女巫布莱尔'
    # #
    # get_single_game = GetSingleGameInfo(game_name=game_name, game_index=1)
    # get_single_game.run()
