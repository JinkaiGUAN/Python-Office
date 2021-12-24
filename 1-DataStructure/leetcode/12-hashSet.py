# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 12-hashSet.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 29/11/2021 22:37 
@Brief   : 
"""
from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar('T')


##### using linkedlist will beyond the time limit.


class Node(Generic[T]):
    def __init__(self, value: T = None, next: Node = None) -> None:
        """

        If you want to create a node instance, please use the example here: `Node[int](1, None)`.

        Args:
            value ():
            next ():
        """
        self.val = value
        self.next = next


class MyHashSet:

    def __init__(self):
        self._base = 769
        self._data = [Node[int](0) for _ in range(self._base)]

    def hash(self, key: int) -> int:
        return key % self._base

    def add(self, key: int) -> None:
        head = self._data[self.hash(key)]
        cur = Node[int](key)
        cur.next = head.next
        head.next = cur

    def remove(self, key: int) -> None:
        head = self._data[self.hash(key)]
        pre = head
        while head.next:
            cur = head.next
            if cur.val == key:
                pre.next = cur.next
                # break, we need to continue this loop so that all nodes with the same key should be deleted
            pre = cur

    def contains(self, key: int) -> bool:
        head = self._data[self.hash(key)]
        while head.next:
            if head.next.val == key:
                return True
            head = head.next
        return False


#### Using bucket

class Bucket(Generic[T]):
    def __init__(self) -> None:
        self.bucket = []

    def update(self, key: T) -> None:
        found = False
        for i, k in enumerate(self.bucket):
            if k == key:
                self.bucket[i] = key
                found = True
                break

        if not found:
            self.bucket.append(key)

    def get(self, key: T) -> bool:
        if key in self.bucket:
            return True
        return False

    def remove(self, key: T) -> None:
        for i, k in enumerate(self.bucket):
            if k == key:
                del self.bucket[i]


class MyHashSetV2:
    def __init__(self):
        self.key_space = 2096
        self.hash_table = [Bucket[int]() for i in range(self.key_space)]

    def hash(self, key: int) -> int:
        return key % self.key_space

    def add(self, key: int) -> None:
        hash_key = self.hash(key)
        self.hash_table[hash_key].update(key)

    def remove(self, key: int) -> None:
        hash_key = self.hash(key)
        self.hash_table[hash_key].remove(hash_key)

    def contains(self, key: int) -> bool:
        hash_key = self.hash(key)
        return self.hash_table[hash_key].get(hash_key)


# Your MyHashSet object will be instantiated and called as such:
obj = MyHashSet()
key = 3
obj.add(key)
obj.remove(key)
param_3 = obj.contains(key)
print(param_3)
