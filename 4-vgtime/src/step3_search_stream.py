# -*- coding: UTF-8 -*-
"""
@Project : 4-vgtime 
@File    : step3_search_stream.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 03/09/2021 09:13 
@Brief   : 
"""
import copy
import math
import os
import random
import threading
import time

import pandas as pd
import numpy as np
from datetime import datetime
import concurrent.futures

from step1_vgtime_parse_2 import create_log_folder


class SearchStream:
    def __init__(self, original_data_path, anchor_data_path, log_folder=None):
        # the final details generated from `vgtime_parse` file.
        self.original_details_path = original_data_path
        # the path stored anchors, and we input it as a excel file
        self.anchor_data_path = anchor_data_path
        # the path we store the game details after filtering
        self.final_details_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'output_files', 'new_details.csv'))
        # the path we put the platforms in the anchor file.
        self.match_data_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'output_files', os.path.basename(anchor_data_path).split('.')[0] + '.csv'))

        if log_folder:
            self.log_path = os.path.join(log_folder, 'match_anchor_log.txt')
        else:
            self.log_path = './match_anchor_log.txt'
        self.lock = threading.Lock()

    def filter_original_data(self):
        """filter the unsatisfied Chinese character and special brackets."""
        details_data = pd.read_csv(self.original_details_path)
        new_details_data = copy.deepcopy(details_data)
        for row_index in new_details_data.index:
            for _, column_index in list(filter(lambda item: item[0] % 2 == 0, enumerate(new_details_data.columns[5:]))):
                if isinstance(details_data.loc[row_index, column_index], float):
                    continue
                elif '最早发售' in new_details_data.loc[row_index, column_index]:
                    new_details_data.loc[row_index, column_index] = \
                        new_details_data.loc[row_index, column_index].replace('\xa0', " ").split(" ")[1]
                elif '(' in new_details_data.loc[row_index, column_index]:
                    new_details_data.loc[row_index, column_index] = \
                        new_details_data.loc[row_index, column_index].split('(')[0]
        new_details_data.to_csv(self.final_details_path, encoding='utf-8', index=False)

        return new_details_data

    def change_xlsx_to_csv(self):
        """Change the anchor list file from excel file into csv file."""
        # data = pd.read_excel(self.anchor_data_path)
        # data.to_csv(self.match_data_path, encoding='utf-8', index=False)

        # return pd.read_csv(self.match_data_path)
        return pd.read_csv(self.anchor_data_path)

    def write_log(self, info):
        self.lock.acquire()
        with open(self.log_path, mode='a', encoding='utf-8', newline='\n') as f:
            f.write("Time: \t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + '\t')
            f.write(info)
            f.write('\n')
        self.lock.release()

    def match_data(self, new_details_data, anchor_list_data):
        for scrapy_index, scrapy_game_name in enumerate(new_details_data.loc[:, 'EnglishName']):
            print("Index = {}\tGameName = {}".format(scrapy_index, scrapy_game_name))
            if isinstance(scrapy_game_name, float) and math.isnan(scrapy_game_name):
                scrapy_game_name = new_details_data.loc[scrapy_index, 'GameName']

            # 获取带有时间的platform
            platform_datetime_list = []
            for _, platform in list(filter(lambda item: item[0] % 2 == 0, enumerate(new_details_data.columns[5:]))):
                date_time_str = new_details_data.loc[scrapy_index, platform]
                if isinstance(date_time_str, str):
                    platform_datetime = None
                    try:
                        platform_datetime = datetime.strptime(date_time_str, '%Y-%m-%d')
                    except:
                        platform_datetime = None
                    finally:
                        if platform_datetime:
                            platform_datetime_list.append((platform, platform_datetime))

            if platform_datetime_list:
                for anchor_index, anchor_game_name in enumerate(anchor_list_data.loc[:, 'game']):
                    # Check if we match the game
                    if scrapy_game_name == anchor_game_name:
                        # 定位当前主播时间
                        anchor_time_str = anchor_list_data.loc[anchor_index, 'date']
                        try:
                            anchor_datetime = datetime.strptime(anchor_time_str, '%Y-%m-%d')
                        except:
                            anchor_datetime = datetime.strptime(anchor_time_str, '%Y-%m-%d %H:%M:%S')

                        mask = anchor_datetime > np.array([platform_date[1] for platform_date in platform_datetime_list])
                        true_platforms = np.array(platform_datetime_list)[mask]
                        if len(true_platforms) > 0:
                            fill_text = random.choice(true_platforms)[0]
                            anchor_list_data.loc[anchor_index, '平台'] = fill_text
                            print("Data filled ---------> ", scrapy_game_name, anchor_index,fill_text)
                    else:
                        info = 'There is no such games in the anchor list for Index = {} with Name = {}'.format(scrapy_index, scrapy_game_name)
                        self.write_log(info)
                        continue
            else:
                info = 'There is no platforms for Index = {} with Name = {}'.format(scrapy_index, scrapy_game_name)
                self.write_log(info)

        return anchor_list_data
        # anchor_list_data.to_csv(self.match_data_path, encoding='utf-8', index=False)

    def run(self):
        # 1. Cut some chinese characters in the csv file and return a new file.
        new_details_data = self.filter_original_data()
        # 2. Change the file type of anchors into csv file.
        anchor_list_data = self.change_xlsx_to_csv()
        # 3. Match data
        anchor_list_data = self.match_data(new_details_data, anchor_list_data)
        # save anchor list data
        anchor_list_data.to_csv(self.match_data_path, encoding='utf-8', index=False)

    def __match_data__(self, new_details_data, scrapy_index, scrapy_game_name):
        print("Index = {}\tGameName = {}".format(scrapy_index, scrapy_game_name))
        if isinstance(scrapy_game_name, float) and math.isnan(scrapy_game_name):
            scrapy_game_name = new_details_data.loc[scrapy_index, 'GameName']

        # 获取带有时间的platform
        platform_datetime_list = []
        for _, platform in list(filter(lambda item: item[0] % 2 == 0, enumerate(new_details_data.columns[6:]))):
            date_time_str = new_details_data.loc[scrapy_index, platform]
            if isinstance(date_time_str, str):
                platform_datetime = None
                try:
                    platform_datetime = datetime.strptime(date_time_str, '%Y-%m-%d')
                except:
                    platform_datetime = None
                finally:
                    if platform_datetime:
                        platform_datetime_list.append((platform, platform_datetime))

        if platform_datetime_list:
            for anchor_index, anchor_game_name in enumerate(self.anchor_list_data.loc[:, 'game']):
                # Check if we match the game
                if scrapy_game_name == anchor_game_name:
                    # 定位当前主播时间
                    anchor_time_str = self.anchor_list_data.loc[anchor_index, 'date']

                    try:
                        anchor_datetime = datetime.strptime(anchor_time_str, '%Y-%m-%d')
                    except:
                        anchor_datetime = datetime.strptime(anchor_time_str, '%Y-%m-%d %H:%M:%S')

                    mask = anchor_datetime > np.array([platform_date[1] for platform_date in platform_datetime_list])
                    true_platforms = np.array(platform_datetime_list)[mask]
                    if len(true_platforms) > 0:
                        fill_text = random.choice(true_platforms)[0]
                        self.anchor_list_data.loc[anchor_index, '平台'] = fill_text
                        print("Data filled ---------> ", scrapy_game_name, anchor_index,fill_text)
                else:
                    # info = 'There is no such games in the anchor list for Index = {} with Name = {}'.format(scrapy_index, scrapy_game_name)
                    # self.write_log(info)
                    continue
        else:
            info = 'There is no platforms for Index = {} with Name = {}'.format(scrapy_index, scrapy_game_name)
            self.write_log(info)

    def main_thread(self):
        # 1. Cut some chinese characters in the csv file and return a new file.
        new_details_data = self.filter_original_data()
        # 2. Change the file type of anchors into csv file.
        self.anchor_list_data = self.change_xlsx_to_csv()
        # 3. Match data
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for scrapy_index, scrapy_game_name in enumerate(new_details_data.loc[:, 'EnglishName']):
                executor.submit(self.__match_data__, new_details_data,scrapy_index, scrapy_game_name)

        self.anchor_list_data.to_csv(self.match_data_path, encoding='utf-8', index=False)


if __name__ == "__main__":
    log_folder_path = create_log_folder()


    original_details_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'input_files','final_details.csv'))
    anchor_data_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'input_files', 'A1_主播表.csv'))

    search_stream = SearchStream(original_details_path, anchor_data_path, log_folder_path)
    # search_stream.run()
    search_stream.main_thread()