# -*- coding: UTF-8 -*-
"""
@Project : 3-Trees 
@File    : _2_binaryTree_base.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 14/10/2021 23:46 
@Brief   : 
"""
from abc import ABC, abstractmethod

from _1_base_trees import Tree, Position


class BinaryTree(Tree, ABC):
    """Abstract base class representing a binary tree structure."""

    @abstractmethod
    def left(self, p: Position):
        """Return a Position representing p's left child.

        Return None if p does not have a left child.
        """
        raise NotImplementedError('Must be implemented by subclass!')

    @abstractmethod
    def right(self, p: Position):
        """Return a Position representing p's right child.

        Return None if p does not have a left child.
        """
        raise NotImplementedError('Must be implemented by subclass!')

    def sibling(self, p: Position):
        """Return a Position representing p's sibling (or None if no sibing)."""
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p: Position):
        """Generate an iteration of Positions representing p's children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p):
            yield self.right(p)

