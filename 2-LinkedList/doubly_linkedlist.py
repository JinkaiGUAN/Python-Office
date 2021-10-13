from singly_linkedlist import Node


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
        node.prev = node.next = node.value = None # deprecate node
        return value


class LinkedDeque(DoublyLinkedList):
    def __init__(self) -> None:
        super().__init__()

    def first(self):
        if self.is_empty():
            raise Exception('Empty queue!')
        return self.header.next.value

    def last(self):
        if self.is_empty():
            raise Exception('Empty queue!')
        return self.trailer.prev.value

    def insert_first(self, value):
        self._insert_between(value, self.header, self.header.next)
    
    def insert_last(self, value):
        self._insert_between(value, self.trailer.prev, self.trailer)

    def delete_first(self):
        if self.is_empty():
            raise Exception('Empty queue!')
        self._delete_node(self.header.next)

    def delete_last(self):
        if self.is_empty():
            raise Exception('Empty queue!')
        self._delete_node(self.trailer.prev)

    

    
    
    

