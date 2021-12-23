# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 21-括号生成.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 23/12/2021 19:40 
@Brief   : https://leetcode-cn.com/leetbook/read/bytedance-c01/eisgxg/
"""
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        if n == 0:
            return []

        # The bracket combination: The index represents n,
        total_brackets = [[None], ["()"]]

        for i in range(2, n+1):
            brackets = []
            for j in range(i):
                now_bracket1 = total_brackets[j]
                now_bracket2 = total_brackets[i-1-j]
                for k1 in now_bracket1:
                    for k2 in now_bracket2:
                        if k1 is None:
                            k1 = ""
                        if k2 is None:
                            k2 = ""
                        el = '(' + k1 + ')' + k2
                        brackets.append(el)
            total_brackets.append(brackets)

        return total_brackets[n]


if __name__ == '__main__':
    print(Solution().generateParenthesis(3))