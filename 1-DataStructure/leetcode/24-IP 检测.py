# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 24-IP 检测.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 24/12/2021 21:36 
@Brief   : https://leetcode-cn.com/leetbook/read/bytedance-c01/eiy7bt/
"""


class Solution:
    def validIPAddress(self, queryIP: str) -> str:
        if queryIP.count('.') == 3:
            return self.validate_IPv4(queryIP)
        elif queryIP.count(':') == 7:
            return self.validate_IPv6(queryIP)
        else:
            return 'Neither'

    def validate_IPv6(self, IP: str) -> str:
        nums = IP.split(':')
        hexdigits = '0123456789abcdefABCDEF'
        for x in nums:
            if len(x) == 0 or len(x) > 4 or not all(c in hexdigits for c in x):
                return 'Neither'

        return 'IPv6'

    def validate_IPv4(self, IP: str) -> str:
        nums = IP.split('.')
        for x in nums:
            if len(x) == 0 or len(x) > 3:
                return 'Neither'
            if x[0] == '0' and len(x) != 1 or not x.isdigit() or int(x) > 255:
                return 'Neither'

        return 'IPv4'


if __name__ == '__main__':
    print(Solution().validIPAddress("172.16.254.1"))
