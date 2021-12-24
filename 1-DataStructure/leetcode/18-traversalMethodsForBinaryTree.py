# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 18-traversalMethodsForBinaryTree.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 07/12/2021 09:39 
@Brief   : This files gives several sorts of methods to traverse a tree.
"""

from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Preorder:
    def solutionRecursion(self, root: TreeNode) -> None:
        if not root:
            return

        print(root.val)
        self.solutionRecursion(root.left)
        self.solutionRecursion(root.right)

    def solutionIteration(self, root: TreeNode) -> None:
        stack = [root]
        while stack:
            s = stack.pop()
            if s:
                print(s.val)
                stack.append(s.right)
                stack.append(s.left)


class Inorder:
    def solutionRecursion(self, root: TreeNode) -> None:
        if not root:
            return

        self.solutionRecursion(root.left)
        print(root.val)
        self.solutionRecursion(root.right)

    def solutionIteration(self, root: TreeNode) -> None:
        stack = []
        while stack or root:
            while root:
                stack.append(root)
                root = root.left

            root = stack.pop()
            print(root.val)
            root = root.right


class PostOrder:
    def solutionRecursion(self, root: TreeNode) -> None:
        if not root:
            return

        self.solutionRecursion(root.left)
        self.solutionRecursion(root.right)
        print(root.val)

    def solutionIteration(self, root: TreeNode) -> None:
        stack = []

        while stack or root:
            while root:
                stack.append(root)
                if root.left:
                    root = root.left
                else:
                    root = root.right

            s = stack.pop()
            print(s.val)

            # If the current node is the left node of previous node, we traverse the right node
            if stack and s == stack[-1].left:
                root = stack[-1].right
            else:
                root = None


class LevelTraversal:
    def solution(self, root: TreeNode) -> None:
        from collections import deque

        queue = deque([root])

        while queue:
            n = len(queue)
            for i in range(n):
                q = queue.popleft()
                if q:
                    print(q.val)
                    queue.append(q.left if q.left else None)
                    queue.append(q.right if q.right else None)


class Depth:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

    def minDepthRecursion(self, root: TreeNode) -> int:
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        if not root.right:
            return 1 + self.minDepthRecursion(root.left)
        if not root.left:
            return 1 + self.minDepthRecursion(root.right)
        return 1 + min(self.minDepthRecursion(root.left), self.minDepthRecursion(root.right))

    def minDepthIteration(self, root: TreeNode) -> int:
        if not root:
            return 0

        ans, count = [root], 1
        while ans:
            n = len(ans)
            for i in range(n):
                r = ans.pop(0)
                if r:
                    if not r.left and not r.right:
                        return count
                    ans.append(r.left if r.left else [])
                    ans.append(r.right if r.right else [])

            count += 1

        return count


class AllRoutes:
    def solution(self, node: TreeNode) -> List:
        if not node.left and not node.right:
            return [str(node.val)]
        left, right = [], []
        if node.left:
            left = [str(node.val) + x for x in self.solution(node.left)]
        if node.right:
            right = [str(node.val) + x for x in self.solution(node.right)]

        return left + right
