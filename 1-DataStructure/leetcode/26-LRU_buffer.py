# -*- coding: UTF-8 -*-
"""
@Project : 1-DataStructure 
@File    : 26-LRU_buffer.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 25/12/2021 22:14 
@Brief   : https://leetcode-cn.com/leetbook/read/bytedance-c01/euhxg3/
"""
from collections import OrderedDict, defaultdict


class LRUCache(OrderedDict):

    def __init__(self, capacity: int):
        super(LRUCache, self).__init__()
        self.capacity = capacity

    def get(self, key: int) -> int:
        """If key is in the buffer, return the value of key, else return -1. You should do it in O(1)."""
        if key not in self:
            return -1

        # move the key to the end
        self.move_to_end(key)

        return self[key]

    def put(self, key: int, value: int) -> None:
        """If key exist, update its value. Otherwise add the new key and its value. If the total length of the buffer
         beyond the maximum capacity, we should pop the least used keywords. You should do it in O(1)."""
        # add and update the key-value
        self.update({key: value})
        # move the key to the end according to the using time
        self.move_to_end(key)
        # remove the key-value once the maximum capacity is up
        if len(self) > self.capacity:
            self.popitem(last=False)


class DoubleLinkedNode:
    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.val = value
        self.prev = None
        self.next = None


class LRUCacheLinkedList:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.size = 0

        self.cache = defaultdict(DoubleLinkedNode)
        # dummy head
        self.head = DoubleLinkedNode()
        # dummy tail
        self.tail = DoubleLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_head(self, node: DoubleLinkedNode) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove_node(self, node: DoubleLinkedNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_to_head(self, node: DoubleLinkedNode) -> None:
        self.remove_node(node)
        self.add_to_head(node)

    def remove_tail(self) -> DoubleLinkedNode:
        node = self.tail.prev
        self.remove_node(node)

        return node

    def get(self, key: int) -> int:
        """If key is in the buffer, return the value of key, else return -1. You should do it in O(1)."""
        if key not in self.cache:
            return -1
        node = self.cache[key]
        # move node to the head
        self.move_to_head(node)

        return node.key

    def put(self, key: int, value: int) -> None:
        """If key exist, update its value. Otherwise add the new key and its value. If the total length of the buffer
         beyond the maximum capacity, we should pop the least used keywords. You should do it in O(1)."""
        if key not in self.cache:
            node = DoubleLinkedNode(key, value)
            self.cache[key] = node
            self.add_to_head(node)
            self.size += 1
            if self.size > self.capacity:
                removed = self.remove_tail()
                self.cache.pop(removed.key)
                self.size -= 1
        else:
            node = self.cache[key]
            node.val = value
            self.move_to_head(node)


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
