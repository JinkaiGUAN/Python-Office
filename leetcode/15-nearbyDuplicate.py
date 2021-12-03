# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 15-nearbyDuplicate.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 03/12/2021 20:32 
@Brief   : 
"""
from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:

        # for i, num1 in enumerate(nums):
        #     if (i + k) > (len(nums) - 1):
        #         slide_window = nums[i+1:]
        #     else:
        #         slide_window = nums[i+1:i + k+1]
        #
        #     for num2 in slide_window:
        #         if num1 == num2:
        #             return True
        #
        # return False

        slide_window = set()
        for i, num in enumerate(nums):
            if num in slide_window:
                return True
            slide_window.add(num)
            if len(slide_window) > k:
                slide_window.remove(nums[i-k])

        return False


if __name__ == '__main__':
    print(Solution().containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2))
