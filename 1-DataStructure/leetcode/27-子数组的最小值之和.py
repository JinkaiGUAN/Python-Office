# -*- coding: UTF-8 -*-
"""
@Project : 1-DataStructure 
@File    : 27-子数组的最小值之和.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 26/12/2021 00:05 
@Brief   : 
"""
from typing import List


class Solution(object):
    def sumSubarrayMins(self, A: List[int]):
        MOD = 10 ** 9 + 7
        N = len(A)

        # prev has i* - 1 in increasing order of A[i*-1], where i* is the answer to query j
        stack = []
        prev = [None] * N

        for i in range(N):
            while stack and A[i] <= A[stack[-1]]:
                stack.pop()

            prev[i] = stack[-1] if stack else -1
            stack.append(i)

        # next has k* + 1 in increasing order of A[k*+1], where k* is the answer to query j
        stack = []
        next_ = [None] * N
        for k in range(N - 1, -1, -1):
            while stack and A[k] < A[stack[-1]]:
                stack.pop()
            next_[k] = stack[-1] if stack else N
            stack.append(k)

        # Use pre/next array to count answer
        return sum((i - prev[i]) * (next_[i] - i) * A[i] for i in range(N)) % MOD


class Solution2:
    MOD = 10 ** 9 + 7

    def sumSubarrayMins(self, A: List[int]) -> int:
        A.append(-1)
        stack, res = [-1], 0
        for i in range(len(A)):
            while A[i] < A[stack[-1]]:
                idx = stack.pop()
                res += A[idx] * (i - idx) * (idx - stack[-1])
            stack.append(i)

        return res % self.MOD


class Solution2Easier:
    MOD = 10 ** 9 + 7

    def sumSubarrayMins(self, A: List[int]) -> int:
        n = len(A)
        if n == 0:
            return 0
        if n == 1:
            return A[0]

        ans = 0
        left = [0] * n
        right = [0] * n

        stack = []
        for i in range(n):
            while stack and A[stack[-1]] > A[i]:
                stack.pop()
            if not stack:
                left[i] = -1
            else:
                left[i] = stack[-1]
            stack.append(i)

        stack = []
        for i in range(n-1, -1, -1):
            while stack and A[stack[-1]] >= A[i]:
                stack.pop()
            if not stack:
                right[i] = n
            else:
                right[i] = stack[-1]
            stack.append(i)

        for i in range(n):
            ans += (i - left[i]) * (right[i] - i) * A[i]



        return ans % self.MOD


if __name__ == '__main__':
    print(Solution2Easier().sumSubarrayMins([71, 55, 82, 55]))
