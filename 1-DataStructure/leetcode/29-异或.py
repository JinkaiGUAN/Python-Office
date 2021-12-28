# -*- coding: UTF-8 -*-
"""
@Project : 1-DataStructure 
@File    : 29-异或.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 28/12/2021 11:43 

0与p异或-> p
p ^ p = 0
p ^ q =
"""
from typing import List


class Solution:

    def singleNonDuplicate(self, nums: List[int]) -> int:

        res = 0
        for num in nums:
            res ^= num

        return res


if __name__ == '__main__':
    nums = [1, 1, 2, 3, 3, 4, 4]
    print(Solution().singleNonDuplicate(nums))