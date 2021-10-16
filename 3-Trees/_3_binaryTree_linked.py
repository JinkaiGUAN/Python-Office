# -*- coding: UTF-8 -*-
"""
@Project : 3-Trees 
@File    : _3_binaryTree_linked.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 15/10/2021 17:26 
@Brief   : 
"""
from abc import ABC
from collections import deque
from typing import Union

import _2_binaryTree_base
from _2_binaryTree_base import BinaryTree


class Node:
    def __init__(self, value, parent=None, left=None, right=None) -> None:
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right


class Position(_2_binaryTree_base.Position, ABC):
    """An abstraction representing the location of a single element. """

    def __init__(self, container: object, node: Node) -> None:
        self.container = container
        self.node = node

    def element(self):
        return self.node.value

    def __eq__(self, other) -> bool:
        """Return True if other is a Position representing the same location."""
        return type(other) is type(self) and other.node == self.node


class LinkedBinaryTree(BinaryTree, ABC):
    def __init__(self):
        self._root = None
        self._size = 0

    def _validate(self, p: Position) -> Node:
        """Return associated node, if position is valid."""
        if not isinstance(p, Position):
            raise TypeError('p must be proper Position type.')
        if p.container is not self:
            raise ValueError('p does not belong to this container.')
        if p.node.parent is p.node:  # convention for deprecated nodes.
            raise ValueError('p is no longer valid.')

        return p.node

    def _make_position(self, node: Node) -> Union[Position, None]:
        """Return position instance for given node (or None if no node)."""
        return Position(self, node) if not node else None

    def __len__(self) -> int:
        return self._size

    def root(self):
        return self._make_position(self._root)

    def parent(self, p: Position):
        node = self._validate(p)
        return self._make_position(node.parent)

    def left(self, p: Position):
        node = self._validate(p)
        return self._make_position(node.left)

    def right(self, p: Position):
        node = self._validate(p)
        return self._make_position(node.right)

    def num_children(self, p: Position):
        node = self._validate(p)
        count = 0
        if node.left:
            count += 1
        if node.right:
            count += 1

        return count

    def _add_root(self, value) -> Position:
        """Place element with value of value at the root of an empty tree and return new Position.

        Raise ValueError if tree nonempty.
        """
        if self._root:
            raise ValueError('Root exits.')
        self._size = 1
        self._root = Node(value)
        return self._make_position(self._root)

    def _add_left(self, p: Position, value) -> Position:
        """Create a new left child for Position p, storing element value.

        Return the Position of the new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node.left:
            raise ValueError('Left child exists.')
        self._size += 1
        node.left = Node(value, parent=p)
        return self._make_position(node.left)

    def _add_right(self, p: Position, value) -> Position:
        """Create a new right child for Position p, storing element value.

        Return the Position of the new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node.right:
            raise ValueError('Right child exists.')
        self._size += 1
        node.right = Node(value, parent=p)
        return self._make_position(node.left)

    def _replace(self, p: Position, value):
        """Replace the element at Position p with value, and return old element."""
        node = self._validate(p)
        old = node.value
        node.value = value
        return old

    def _delete(self, p: Position):
        """Delete the node at Position p, and replace it with its child, if any.

        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children.')

        child = node.left if node.left else node.right

        if child:
            child.parent = node.parent
        if node is self._root:
            self._root = child
        else:
            parent = node.parent
            if node is parent.left:
                parent.left = child
            else:
                parent.right = child
        self._size -= 1
        node.parent = node  # convention for deprecate node
        return node.value

    def _attach(self, p: Position, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('Position must be leaf.')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must match.')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root.parent = node
            node.left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root.parent = node
            node.right = t2._root
            t2._root = None
            t2._size = 0

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for p in self.position():
            yield p.element()

    from typing import Iterator

    def position(self) -> Iterator[Position]:
        """Generates an iteration of the tree's positions."""
        return self.preorder()

    def preorder(self) -> Iterator[Position]:
        """Generate a preorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self, p: Position) -> Iterator[Position]:
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def postorder(self) -> Iterator[Position]:
        """Generate a postorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p: Position) -> Iterator[Position]:
        """Generate a postorder iteration of positions in subtree rooted at p."""
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other

        yield p

    def inorder(self) -> Iterator[Position]:
        """Generate a inorder iteration of positions in the tree.

        Notes: Please be careful to define this method since such a method can only be used in the binary tree class.
        """
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p: Position) -> Iterator[Position]:
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.left(p):
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p
        if self.right(p):
            for other in self._subtree_inorder(self.right(p)):
                yield other

    def bfs(self) -> Iterator[Position]:
        """Generate a breadth-first iteration of the positions of the tree."""
        if not self.is_empty():
            fringe = deque()
            fringe.append(self.root())
            while not len(fringe) == 0:
                p = fringe.popleft()
                yield p

                for c in self.children(p):
                    fringe.append(c)
