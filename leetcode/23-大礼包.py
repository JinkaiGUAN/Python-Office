# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 23-大礼包.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 23/12/2021 23:16 
@Brief   : https://leetcode-cn.com/leetbook/read/bytedance-c01/ei1ujj/
"""
from typing import List, Tuple, Any, Union
from functools import lru_cache


class Solution:
    def shoppingOffers(self, price: List[int], special: List[List[int]], needs: List[int]) -> int:
        n = len(price)

        # filter improper specials
        filter_special = []
        for sp in special:
            # The goods number should be larger than zero and total price of all goods should be larger than the
            # special price.
            if sum(sp[:-1]) > 0 and sum(sp[i] * price[i] for i in range(n)) > sp[-1]:
                filter_special.append(sp)

        @lru_cache(None)
        def dfs(cur_needs: Tuple[int, ...]) -> int:
            # Calculate the minimum price without using any specials
            min_price = sum(need * price[i] for i, need in enumerate(needs))

            for cur_special in filter_special:
                special_price = cur_special[-1]
                nxt_needs = []
                for i in range(n):
                    # The goods number in the special list should not be larger than that in the needs
                    if cur_special[i] > cur_needs[i]:
                        break
                    nxt_needs.append(cur_needs[i] - cur_special[i])

                # We can buy this special
                if len(nxt_needs) == n:
                    min_price = min(min_price, dfs(tuple(nxt_needs)) + special_price)

            return min_price

        return dfs(tuple(needs))


if __name__ == '__main__':
    a = [2, 5]
    b = [[3, 0, 5], [1, 2, 10]]
    c = [3, 2]

    print(Solution().shoppingOffers(a, b, c))  # should be 14
