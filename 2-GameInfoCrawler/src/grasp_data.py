# -*- coding: UTF-8 -*-
"""
@Project : 2-GameInfoCrawler 
@File    : grasp_data.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 31/08/2021 16:29 
@Brief   : 
"""
import pandas as pd
import time
import csv
import os

from test_latin import GetSingleGameInfo


if __name__ == "__main__":
    name_interval = 10 # 每次运行爬取十个游戏

    # with open(os.path.abspath(os.path.join(os.getcwd(), '..', 'NewGameList.csv')))
    game_list_data = pd.read_csv(os.path.abspath(os.path.join(os.getcwd(), '..', 'NewGameList.csv')))
    """
    1. index = 370 name = 战火兄弟连 30高地之路, offset = 369
    """

    # offset = 0
    # index = 690 西部旋转侠 最后的保镖 offset= 689
    offset = 369

    game_name_data = game_list_data.loc[:, 'GameName'][0:700]

    for index, game_name in enumerate(game_name_data):
        if (index + 1 + offset) % 50 == 0 and offset != 0:
            print("<--------------------- Pause the Machine --------------------->")
            print("Time: \t" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            time.sleep(300)

        print(index+1 + offset, game_name,)
        time_start = time.time()
        try:
            get_single_game = GetSingleGameInfo(game_name=game_name, game_index=index+1 + offset)
            # get_single_game.run()
            get_single_game.main_thread()
            print("Time used: ", time.time() - time_start)
            time.sleep(10)
        except Exception as e:
            print("Time used: ", time.time() - time_start)
            raise e


