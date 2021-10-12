from typing import Any


class Node:
    __slots__ = ('value', 'next')  # constrict the variables can be used in this class

    def __init__(self, element:Any, next=None) -> None:
        self.value = element
        self.next = next


class LinkedStack:
    """LIFO Stack implementation using a singly linked list for storage."""

    def __init__(self, value: Any = None) -> None:
        if value:
            self.head = Node(value)
            self.size = 1

        self.head = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        return self.size == 0

    def push(self, value: Any) -> None:
        if not value:
            raise ValueError(f'Please input value value, we got {value}.')
        self.head = Node(value, self.head)
        self.size += 1

    def top(self) -> Any:
        if self.is_empty():
            raise Exception('Stack is empty!')
        
        return self.head.value

    def pop(self) -> Any:
        """Remove and return the element from the top of the stack, i.e., the head of this singly linked list.

        Raises:
            Exception: [description]

        Returns:
            Any: [description]
        """
        if self.is_empty():
            raise Exception('Stack is empty!')

        answer = self.head.value
        self.head = self.head.next
        self.size -= 1

        return answer
        
