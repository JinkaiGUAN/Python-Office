from singly_linkedlist import Node


class CircularQueue:
    def __init__(self) -> None:
        self.tail = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        return self.size == 0

    def first(self):
        if self.is_empty():
            raise Exception('Empty queue!')
        return self.tail.next.value

    def dequeue(self):
        if self.is_empty():
            raise Exception('Empty queue!')

        old_node = self.tail.next
        if self.size == 1:
            self.tail = None
        else:
            self.tail = old_node.next
        self.size -= 1

        return old_node.value

    def enqueue(self, value):
        new_node = Node(value)

        if self.is_empty():
            new_node.next = new_node
        else:
            self.tail.next = new_node
            new_node.next = self.tail.next

        self.tail = new_node
        self.size += 1

    def rotate(self):
        """Rotate front element to the back of the queue."""
        if self.size > 0:
            # heare we simply need to update the tail pointer.
            self.tail = self.tail.next  # old head becomes new tail

    