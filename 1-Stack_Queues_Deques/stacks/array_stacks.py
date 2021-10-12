from typing import Any


class Empty(Exception):
    """Error attemping to access an element from an empty container."""
    pass


class ArrayStack:
    """LIFO (Last input first output) Stack implementation using a Python list a underlying storage."""

    def __init__(self) -> None:
        """Create an empty stack."""
        self.__data = []

    def __len__(self) -> int:
        return len(self.__data)

    def is_empty(self) -> bool:
        return len(self.__data) == 0

    def push(self, value: Any) -> None:
        """Add element value to the top of the stack."""
        self.__data.append(value)
        
    def top(self):
        """Return (but do not move) the element at the top of the stack.
        
        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty!')

        return self.__data[-1]

    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO)

        Raise Empty Exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty!')
        
        return self.__data.pop()




