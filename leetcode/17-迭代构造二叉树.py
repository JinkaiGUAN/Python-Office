# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 17-迭代构造二叉树.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 06/12/2021 11:52 
@Brief   : 使用前序和中序便利结构构造二叉树
"""

from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        if not preorder:
            return None

        root = TreeNode(preorder[0])
        stack = [root]
        inorderIndex = 0
        for i in range(1, len(preorder)):
            preorderVal = preorder[i]
            node = stack[-1]
            if node.val != inorder[inorderIndex]:
                node.left = TreeNode(preorderVal)
                stack.append(node.left)
            else:
                while stack and stack[-1].val == inorder[inorderIndex]:
                    node = stack.pop()
                    inorderIndex += 1
                node.right = TreeNode(preorderVal)
                stack.append(node.right)

        return root


if __name__ == '__main__':
    """
            3
           / \
          9  20
         /  /  \
        8  15   7
       / \
      5  10
     /
    4
    """
    preorder = [3, 9, 8, 5, 4, 10, 20, 15, 7]
    inorder = [4, 5, 8, 10, 9, 3, 15, 20, 7]

    Solution().buildTree(preorder, inorder)