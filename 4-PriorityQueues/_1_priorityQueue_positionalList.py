# -*- coding: UTF-8 -*-
"""
@Project : 4-PriorityQueues 
@File    : _1_priorityQueue_positionalList.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 17/10/2021 11:06 
@Brief   : 
"""
# import sys
# import os
# BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
# sys.path.append(BASE_DIR)
# from baseStructures._1_positioanl_list import PositionalList
from _1_positioanl_list import PositionalList, Position


class Item:
    def __init__(self, k, v):
        self._key = k
        self._value = v

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def __lt__(self, other):
        return self._key < other.key


class PriorityQueueBase:
    """Abstract base class for a priority queue."""

    def is_empty(self):
        """Return True if the priority queue is empty."""
        return len(self) == 0


class UnsortedPriorityQueue(PriorityQueueBase):
    def __init__(self):
        super(UnsortedPriorityQueue, self).__init__()
        self._data = PositionalList()

    def _find_min(self) -> Position:
        """Return Position of item with minimum key."""
        if self.is_empty():
            raise Exception('Priority queue is empty.')
        small = self._data.first()
        walk = self._data.after(small)
        while walk:
            if walk.value() < small.value():
                small = walk
            walk = self._data.after(walk)

        return small

    def __len__(self) -> int:
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, k, v):
        """Add a key-value pair."""
        self._data.add_last(Item(k, v))

    def min(self):
        """Return but do not remove (k, v) tuple with minimum key."""
        p = self._find_min()
        item = p.element()
        return item.key, item.value

    def remove_min(self):
        """Remove and return (k, v) tuple with minimum key."""
        p = self._find_min()
        item = self._data.delete(p)
        return item.key, item.value



