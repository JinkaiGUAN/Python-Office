from typing import List


class Solution:
    """https://leetcode-cn.com/leetbook/read/binary-search/xenp13/"""

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # When nums is none, we will do nothing, just retrun [-1, -1]
        if not nums:
            return [-1, -1]

        def binary_search(nums: List[int], target: int, lower: bool) -> int:
            """Return the boundary, i.e., the index of the first number greater than the target, and the index of the 
            last number that eauual to the target.
            
                lower(bool): This is used to control where we are going to find the index of number that equal to or 
                 greater than the target. Or we will focus on finding the number lager than the target.
            """
            left, right = 0, len(nums) - 1
            ans = len(nums)

            while left <= right:
                mid = (left + right) // 2
                if (nums[mid] > target or (lower and (nums[mid] >= target))):
                    right = mid - 1
                    ans = mid if lower else mid - 1
                else:
                    left = mid + 1

            if ans >= len(nums):
                ans = ans - 1
            return ans
        
        left_idx = binary_search(nums, target, True)
        right_idx = binary_search(nums, target, False)

        if left_idx <= right_idx and right_idx < len(nums) and nums[left_idx] == target and nums[right_idx] == target:
            return [left_idx, right_idx]
        return [-1, -1]


print(Solution().searchRange([1], 1))