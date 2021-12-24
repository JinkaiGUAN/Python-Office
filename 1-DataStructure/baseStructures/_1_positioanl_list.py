# -*- coding: UTF-8 -*-
"""
@Project : baseStructures 
@File    : _1_positional_list.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 17/10/2021 11:16 
@Brief   : Base file stores basic data structures for liked list.
"""
from typing import Any, Union


class Node2:
    def __init__(self, value, prev=None, next=None) -> None:
        self.value = value
        self.prev = prev
        self.next = next


class DoublyLinkedList:

    def __init__(self) -> None:
        self.header = Node2(None, None, None)
        self.trailer = Node2(None, None, None)
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def _insert_between(self, value, pre_node: Node2, next_node: Node2) -> Node2:
        new_node = Node2(value, pre_node, next_node)
        pre_node.next = next_node
        next_node.prev = new_node
        self.size += 1

        return new_node

    def _delete_node(self, node: Node2):
        predecessor = node.prev
        successor = node.next

        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1

        value = node.value
        node.prev = node.next = node.value = None  # deprecate node
        return value


class Position:
    """An abstraction representing the location of a single element."""

    def __init__(self, container=None, node: Any = None) -> None:
        """[summary]

        Args:
            container ([type], optional): [description]. Defaults to None.
            node (Any, optional): node can be any kinds of basic class. Defaults to None.
        """
        self.container = container
        self.node = node

    def element(self):
        return self.node

    def value(self):
        return self.node.value

    def __eq__(self, other) -> bool:
        """Return true if other is a Position representing the same location."""
        return type(other) is type(self) and other.node is self.node

    def __ne__(self, other: object) -> bool:
        """"Return true if other does not represent the same location."""
        return not (self == other)


class PositionalList(DoublyLinkedList):
    """A sequential container of elements allowing positional access."""

    def __init__(self) -> None:
        super().__init__()

    def _validate(self, p: Position) -> Node2:
        """Return position's node, or raise appropriate error is invalid."""
        if not isinstance(p, Position):
            raise TypeError('p must be proper Position type')
        if p.container is not self:
            raise ValueError('P does not belong to this container.')
        if p.node.next is None:
            raise ValueError('p is no longer valid!')
        if p.node.prev is None:
            raise ValueError('p is no longer valid!')

        return p.node

    def _make_position(self, node) -> Union[Position, None]:
        """Return Position instance for geiven node (or None if sentinel)."""
        if node is self.header or node is self.trailer:
            return None  # boundary violcation
        else:
            return Position(self, node)  # legitimate position

    def first(self) -> Position:
        """Return the first Posioton in the list (or None is list is empty)."""
        return self._make_position(self.header.next)

    def last(self) -> Position:
        """Return the last Posioton in the list (or None is list is empty)."""
        return self._make_position(self.trailer.prev)

    def before(self, p: Position) -> Position:
        """Return the Position just before Posion p (or None if p is first)."""
        node = self._validate(p)

        return self._make_position(node.prev)

    def after(self, p: Position) -> Position:
        """Return the Position just afetr Posion p (or None if p is last)."""
        node = self._validate(p)
        return self._make_position(node.next)

    def __iter__(self):
        """Generate a forward iteration of the elements of the list."""
        cursor = self.first()

        while cursor is not None:
            yield cursor.value()
            cursor = self.after(cursor)

    def _insert_between(self, value, pre_node: Node2, next_node: Node2) -> Position:
        node = None
        if isinstance(value, (int, float, str)):
            node = super()._insert_between(value, pre_node, next_node)
        if isinstance(value, object):
            # At this case, the input value is a object, i.e., it can be a node, then we just return it self.
            node = node
        return self._make_position(node)

    def add_first(self, value) -> Position:
        """Insert element value at the front of the list and return new Position."""
        return self._insert_between(value, self.header, self.header.next)

    def add_last(self, value) -> Position:
        """Insert element value at the end of the list and return new Position."""
        # return self._make_position(value)
        return self._insert_between(value, self.trailer.prev, self.trailer)

    def add_before(self, p: Position, value) -> Position:
        """Insert element value into list before Position p and return new Position."""
        original_node = self._validate(p)
        return self._insert_between(value, original_node.prev, original_node)

    def add_after(self, p: Position, value) -> Position:
        """Insert element value into list after Position p and return new Position."""
        original_node = self._validate(p)
        return self._insert_between(value, original_node, original_node.next)

    def delete(self, p: Position):
        """Remove and return the element at Position p."""
        original_node = self._validate(p)
        return self._delete_node(original_node)

    def replace(self, p: Position, value):
        """Replace the element at Position p with value.

        Return the value formerly at Position p.
        """
        original_node = self._validate(p)
        old_value = original_node.value
        original_node.value = value

        return old_value
