# -*- coding: UTF-8 -*-
"""
@Project : 1-DataStructure 
@File    : 3.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 02/03/2022 17:16 
@Brief   : 
"""


# If you need to import additional packages or classes, please import here.
import typing as t

class Solution:
    def __init__(self, consumer_num: int, time_series_list: t.List[t.List[int]]) -> None:
        self._consumer_num = consumer_num
        self._time_series = time_series_list

    def sort_time_series(self):
        def sorting_way(x):
            if x[0]

        sorted(self._time_series, lambda x: x[0] )





def func():

    # please define the python3 input here. For example: a,b = map(int, input().strip().split())
    # please finish the function body here.
    # please define the python3 output here. For example: print().
    consumer_num = int(input())
    time_series = input().split(" ")

    # handle the time series and store them in a list
    time_series_list = [[int(time_series[2 * i]), int(time_series[2 * i + 1])] for i in range(consumer_num)]

    solution = Solution(consumer_num, time_series_list)



if __name__ == "__main__":
    func()
