# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 20-数组的最小偏移量.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 22/12/2021 19:34 
@Brief   : https://leetcode-cn.com/leetbook/read/bytedance-c01/eigcei/
"""
from typing import List
import heapq


class Solution:
    def minimumDeviation(self, nums: List[int]) -> int:
        queue = []
        # Make all nums even
        for num in nums:
            if num % 2 != 0:
                heapq.heappush(queue, num * 2)
            else:
                heapq.heappush(queue, num)

        # The offset between the largest and smallest
        res = heapq.nlargest(1, queue)[0] - heapq.nsmallest(1, queue)[0]

        while res > 0 and heapq.nlargest(1, queue)[0] % 2 == 0:
            max_num = heapq.nlargest(1, queue)[0]
            queue.remove(max_num)
            queue.append(max_num // 2)
            res = min(res, heapq.nlargest(1, queue)[0] - heapq.nsmallest(1, queue)[0])

        return res


if __name__ == '__main__':
    a = [4, 1, 5, 20, 3]
    print(Solution().minimumDeviation(a))
