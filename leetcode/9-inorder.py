from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        ### Recursion

        # array = []
        # def inorder(root: TreeNode) -> None:
        #     if root:
        #         inorder(root.left)
        #         array.append(root.val)
        #         inorder(root.right)

        # inorder(root)
        # return array
        
        ### Iterative 

        res = []
        stack = []  # storing all nodes when using iterative way

        while root is not None or len(stack) != 0:
            while root is not None:
                stack.append(root)
                root = root.left
            root = stack.pop()
            res.append(root.val)
            root = root.right
        return res



