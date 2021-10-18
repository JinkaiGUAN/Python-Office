# -*- coding: UTF-8 -*-
"""
@Project : 4-PriorityQueues 
@File    : _2_heap.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 18/10/2021 09:54 
@Brief   : 
"""

from _1_priorityQueue_positionalList import PriorityQueueBase, Item


class HeapPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue based on array implemented with a binary heap."""

    def __init__(self):
        self._data = []

    def _parent(self, j):
        return (j - 1) // 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        """Swap the elements at indices i and j of array."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        """Change the position of index j according to the order property. This method is going up to swap the entry."""
        parent = self._parent(j)
        if j > 0 and self._data[parent] > self._data[j]:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        """Change the position of index j according to the order property. This method is going down to swap the
         entry."""
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    def __len__(self):
        return len(self._data)

    def add(self, key, value):
        self._data.append(Item(key, value))
        self._upheap(len(self._data) - 1)

    def min(self):
        """
        Return but do not remove (k, v) tuple with minimum key.

        Raise error if empty.
        """
        if self.is_empty():
            raise Exception('Heap is empty!')
        item = self._data[0]
        return item.key, item.value

    def remove_min(self):
        """
        Return and remove (k, v) tuple with minimum key.

        Raise error if empty.
        """
        if self.is_empty():
            raise Exception('Heap is empty!')
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        self._downheap(0)
        return item.key, item.value
