# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 19-放置盒子.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 20/12/2021 18:36 
@Brief   : https://leetcode-cn.com/leetbook/read/bytedance-c01/eikfoc/
"""


class Solution:
    def minimumBoxes(self, n: int) -> int:
        level, cnt = 1, 0

        # Find the level resulting in the box number is less than or equal to the total one.
        while cnt + (1 + level) * level // 2 <= n:
            cnt += (1 + level) * level // 2
            level += 1
        level -= 1

        # the box number stick to the earth
        area = (1 + level) * level // 2

        x = 0
        while cnt + (1 + x) * x // 2 < n:
            x += 1
        area += x

        return area


if __name__ == '__main__':
    print(Solution().minimumBoxes(15))
