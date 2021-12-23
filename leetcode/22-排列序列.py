# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 22-排列序列.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 23/12/2021 22:31 
@Brief   : https://leetcode-cn.com/leetbook/read/bytedance-c01/ei4qhv/
"""
from typing import List


def getFactorial(num: int) -> int:
    if num == 0:
        return 1

    factorial = 1
    for i in range(1, num+1):
        factorial *= i

    return factorial


class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        """

        Args:
            n (): The largest number.
            k (): kth number we are going to get.

        Returns:
            str, the number we want.
        """
        # The original set
        nums = list(range(1, n+1))
        # res
        res: List[str] = []

        while n:
            # Find the index
            a = int((k-1) / getFactorial(n - 1))
            res.append(str(nums[a]))
            nums.pop(a)

            # update n and k
            k = (k - 1) % getFactorial(n-1) + 1
            n -= 1

        return ''.join(res)


if __name__ == '__main__':
    print(Solution().getPermutation(3, 3))
