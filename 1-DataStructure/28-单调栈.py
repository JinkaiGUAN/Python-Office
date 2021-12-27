# -*- coding: UTF-8 -*-
"""
@Project : 1-DataStructure 
@File    : 28-单调栈.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 26/12/2021 17:56 
@Brief   : 单调栈 (Monotonic stack) - 栈中元素， 按递增顺序或者递减顺序排列的时候， 是否严格递增或者non-decreasing （具体取决于题目）。
            优势是时间复杂度是线性的， 每个元素遍历一次。
"""

"""
输入数组 nums = [2, 1, 2, 4, 3], 返回数组 [4, 2, 4, -1, -1].

Explanation: 第一个2后面比2大的树是4， 1后面比1大的数是2， 第二个2后面比2大的数是4， 4后面没有比4大的数， 填-1， 3后面没有比3大的数， 填-1.

三步走：
1. 维持递增栈。
2. 放入最后结果array。
3. 当前元素入栈。

Template - Java
private static int[] nextGreaterElement(int[] nums) {
        int[] res = new int[nums.length];
        Stack<Integer> stack = new Stack<>();
        for (int i = nums.length - 1; i >= 0; i--) {
            while (!stack.isEmpty() && nums[i] >= stack.peek()) {
                stack.pop();
            }
            res[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(nums[i]);
        }
        return res;
}
"""


