# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 14-inheitance_property.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 03/12/2021 15:47 
@Brief   : 
"""


class Father:
    def __init__(self, value):
        self.val = value

    @property
    def value(self):
        return self.val


class Son(Father):
    def __init__(self, value):
        super(Son, self).__init__(value)
        print(self.__class__.__name__, 2, self.value)


class ChildSon(Son):
    def __init__(self, value):
        super(ChildSon, self).__init__(value)
        print(self.__class__.__name__, 1, self.value)


if __name__ == '__main__':
    childSon = ChildSon(5)