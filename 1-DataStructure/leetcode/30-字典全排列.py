# -*- coding: UTF-8 -*-
"""
@Project : 1-DataStructure 
@File    : 30-字典全排列.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 27/02/2022 23:47 
@Brief   : 
"""


class DictPermutation:
    def __init__(self):
        self.params = {
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "C": [7, 8]
        }

        self.res = []
        self.path = {}

    def back_tracking(self, key, start_idx):
        # todo: check the returning condition

        for i in range(start_idx, len(self.params[key])):
            self.path[key] = self.params[key][i]
            self.back_tracking(key, i + 1)
            self.path.pop(key)

    def outside_back_tracking(self, key):
        if len(self.path) == len(self.params):
            self.res.append(self.path.copy())
            self.path.clear()
            return

        for key, vals in self.params:
            pass


my_dict = {
    "A": [1, 2, 3],
    "B": [4, 5, 6],
    "C": [7, 8]
}

res = [[]]
for _, vals in my_dict.items():

    res = [x + [y] for x in res for y in vals]
print(res)
