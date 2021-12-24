from typing import Any
from stacks.array_stacks import Empty


class ArrayQueue:
    DEFAULT_CAPACITY = 10

    def __init__(self) -> None:
        self.__data = [None] * self.DEFAULT_CAPACITY
        self.__size = 0
        self.__front = 0

    def __len__(self) -> int: 
        return self.__size

    def is_empty(self) -> bool:
        return self.__size == 0

    def first(self) -> Any:
        if self.is_empty():
            raise Empty('Queue is empty')
        return self.__data[self.__front]

    def dequeue(self) -> Any:
        """Remove the first element of the queue.

        Raises:
            Empty: [description]

        Returns:
            Any: [description]
        """
        if self.is_empty():
            raise Empty('Queue is empty')

        answer, self.__data[self.__front] = self.__data[self.__front], None
        self.__front = (self.__front + 1) % len(self.__data)
        self.__size -= 1

        return answer

    def enqueue(self, value: Any) -> Any:
        """Add element value into the queue.

        Args:
            value (Any): [description]

        Returns:
            Any: [description]
        """
        if self.__size == len(self.__data):
            self._resize(2 * len(self.__data))
        avail = (self.__front + self.__size) % len(self.__data)
        self.__data[avail] = value
        self.size += 1

    def _resize(self, cap: int):
        old, self.__data = self.__data, [None] * cap
        walk = self.__front
        for k in range(self.__size):
            self.__data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self.__front = 0

    

