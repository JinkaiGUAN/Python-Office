from typing import Type
from doubly_linkedlist import DoublyLinkedList
from singly_linkedlist import Node
from doubly_linkedlist import Node2


class Position:
    """An abstraction representing the location of a single element."""
    def __init__(self, container=None, node: Node2=None) -> None:
        self.container = container
        self.node = node

    def element(self):
        return self.node.value

    def value(self):
        return self.node.value

    def __eq__(self, other) -> bool:
        """Return true if other is a Position representing the same location."""
        return type(other) is type(self) and other.node is self.node

    def __ne__(self, other: object) -> bool:
        """"Return true if other does not represent the same location."""
        return not (self == other)    


class PositionalList(DoublyLinkedList):
    """A sequential container of elements allowing positional access."""

    def __init__(self) -> None:
        super().__init__()

    def _validate(self, p: Position) -> Node2: 
        """Return position's node, or raise appropriate error is invalid."""
        if not isinstance(p, Position):
            raise TypeError('p must be proper Position type')
        if p.container is not self:
            raise ValueError('P does not belong to this container.')
        if p.node.next is None:
            raise ValueError('p is no longer valid!')
        if p.node.prev is None:
            raise ValueError('p is no longer valid!')

        return p.node

    def _make_postion(self, node) -> Position:
        """Return Position instance for geiven node (or None if sentinel)."""
        if node is self.header or node is self.trailer:
            return None  # boundary violcation
        else:
            return Position(self, node)  # legitimate position

    def first(self) -> Position:
        """Return the first Posioton in the list (or None is list is empty)."""
        return self._make_postion(self.header.next)

    def last(self) -> Position:
        """Return the last Posioton in the list (or None is list is empty)."""
        return self._make_postion(self.trailer.prev)

    def before(self, p: Position) -> Position:
        """Return the Position just before Posion p (or None if p is first)."""
        node = self._validate(p)

        return self._make_postion(node.prev)

    def after(self, p: Position) -> Position:
        """Return the Position just afetr Posion p (or None if p is last)."""
        node = self._validate(p)
        return self._make_postion(node.next)

    def __iter__(self):
        """Generate a forward iteration of the elements of the list."""
        cursor = self.first()

        while cursor is not None:
            yield cursor.value()
            cursor = self.after(cursor)

    def _insert_between(self, value, pre_node: Node2, next_node: Node2) -> Node2:
        node = super()._insert_between(value, pre_node, next_node)
        return self._make_postion(node)

    def add_first(self, value) -> Position:
        """Insert element value at the front of the list and return new Position."""
        return self._insert_between(value, self.header, self.header.next)

    def add_last(self, value) -> Position:
        """Insert element value at the end of the list and return new Position."""
        return self._make_postion(value, self.trailer.prev, self.trailer)

    def add_before(self, p: Position, value) -> Position:
        """Insert element value into list before Position p and return new Position."""
        original_node = self._validate(p)
        return self._insert_between(value, original_node.prev, original_node)

    def add_after(self, p: Position, value) -> Position:
        """Insert element value into list after Position p and return new Position."""
        original_node = self._validate(p)
        return self._insert_between(value, original_node, original_node.next)

    def delete(self, p: Position):
        """Remove and return the element at Position p."""
        original_node = self._validate(p)
        return self._delete_node(original_node)

    def replace(self, p: Position, value):
        """Replace the element at Positon p with value.
        
        Retunr the value formerly at Position p."""
        original_node = self._validate(p)
        old_value = original_node.value
        original_node.vlaue = value

        return old_value
        