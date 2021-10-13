from typing import Any, Union


class Node:
    __slots__ = ('value', 'next')  # constrict the variables can be used in this class

    def __init__(self, element:Any, next=None) -> None:
        self.value = element
        self.next = next


class LinkedListStack:
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
        

class LinkedListQueue:
    def __init__(self, value: Union[float, int, str]) -> None:
        """FIFO queue implementation using a singly linked list for storage."""
        if value:
            self.head = self.tail = Node(value)
            self.size = 1

        self.head = None
        self.tail = None
        self.size  = 0

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        return self.size == 0

    def first(self) -> Union[float, int, str]:
        if self.is_empty():
            raise Exception('The queue is empty!')
        
        return self.head.value

    def dequeue(self) -> Union[float, int, str]:
        """Remove and return the first element of the queue (i.e., FIFO).

        Raises:
            Exception: Raise exception is the queue is empty.

        Returns:
            Union[float, int, str]: [description]
        """
        if self.is_empty():
            raise Exception('The queue is empty!')

        answer = self.head.value
        self.head = self.head.next
        self.size -= 1
        if self.is_empty():
            self.tail = None
        
        return answer

    def enqueue(self, value: Union[float, int, str]) -> None:
        new_node = None(value)
        if self.is_empty():
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        
        self.size += 1


