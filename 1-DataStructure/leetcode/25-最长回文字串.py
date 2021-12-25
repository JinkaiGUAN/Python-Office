# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 25-最长回文字串.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 25/12/2021 09:57 
@Brief   : https://leetcode-cn.com/leetbook/read/bytedance-c01/eijp4d/
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n < 2:
            return s
        max_len = 1
        begin = 0

        # Add DP matrix
        dp = [[False] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = True

        for L in range(2, n+1):
            # The length of sub-string
            for i in range(n):
                # L = j - i + 1
                j = L + i - 1

                # break the bound
                if j >= n:
                    break

                if s[i] != s[j]:
                    dp[i][j] = False
                else:
                    if j - i < 3:
                        dp[i][j] = True
                    else:
                        dp[i][j] = dp[i + 1][j - 1]

                if dp[i][j] and j - i + 1 > max_len:
                    max_len = j - i + 1
                    begin = i

        return s[begin: begin+max_len]


if __name__ == '__main__':
    print(Solution().longestPalindrome("bb"))