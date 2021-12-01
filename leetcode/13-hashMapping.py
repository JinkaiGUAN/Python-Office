# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 13-hashMapping.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 01/12/2021 21:22 
@Brief   : 
"""

class MyHashMap:
    """
    The main difference between hashMapping and hashSet is that hasMapping stores key value pair, while hashSet stores
    key.

    """

    def __init__(self):
        self.base = 1009
        self.table = [[] for _ in range(self.base)]

    def _hash_(self, key: int) -> int:
        return key % self.base

    def put(self, key: int, value: int) -> None:
        hash_key = self._hash_(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                item[1] = value
                return

        self.table[hash_key].append([key, value])

    def get(self, key: int) -> int:
        hash_key = self._hash_(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                return item[1]

        return -1

    def remove(self, key: int) -> None:
        hash_key = self._hash_(key)
        for i, item in enumerate(self.table[hash_key]):
            if item[0] == key:
                self.table[hash_key].pop(i)
                return
