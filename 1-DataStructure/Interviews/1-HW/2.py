# -*- coding: UTF-8 -*-
"""
@Project : 1-DataStructure 
@File    : 2.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 02/03/2022 16:24 
@Brief   : 
"""

import typing as t


class Solution:
    def __init__(self, versions: t.List[str]) -> None:
        self._versions = versions

    def compare(self, str1: str, str2: str) -> bool:
        """Compare str1 and str2, return True if the version of str1 is larger than or equal to that of str2."""
        # check the feeding input is legal or not
        str1s, str2s = str1.split('.'), str2.split('.')

        # transfer string into a list
        nums1, nums2 = self.__strs2nums__(str1s), self.__strs2nums__(str2s)

        # compare the version
        for num1, num2 in zip(nums1, nums2):
            if num1 < num2:
                return False

        return True

    def __strs2nums__(self, strs: t.List[str]) -> t.List[int]:
        nums = []

        for s in strs:
            if s is None:
                nums.append(0)
            elif s == '':
                nums.append(0)
            else:
                # python int helps us to filter the prefix zeros
                nums.append(int(s))

        return nums

    def quick_sort(self, versions: t.List[str], i: int, j: int):
        """Sort the version list ascenddingly."""
        if i >= j:
            return versions

        # Set a comparison mark
        pivot = versions[i]

        # Set the limits
        low, high = i, j

        while i < j:
            while i < j and self.compare(versions[j], pivot):
                j -= 1
            versions[i] = versions[j]
            while i < j and self.compare(pivot, versions[i]):
                i += 1
            versions[j] = versions[i]
        versions[j] = pivot

        self.quick_sort(versions, low, i - 1)
        self.quick_sort(versions, i + 1, high)

        return versions

    def run(self):
        """Main function to achieve the function."""
        res = self.quick_sort(self._versions, 0, len(self._versions) - 1)[::-1]
        for str in res:
            print(str)


def func():
    # please define the python3 input here. For example: a,b = map(int, input().strip().split())
    # please finish the function body here.
    # please define the python3 output here. For example: print().
    # Read the stream
    version_num = int(input())
    i = 0  # recore the line we are reading

    versions = []
    while i < version_num:
        versions.append(input())
        i += 1

    solution = Solution(versions)
    solution.run()


if __name__ == "__main__":
    func()
