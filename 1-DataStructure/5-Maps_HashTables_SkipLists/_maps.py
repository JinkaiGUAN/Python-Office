# -*- coding: UTF-8 -*-
"""
@Project : 5-Maps_HashTables_SkipLists 
@File    : _maps.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 19/10/2021 17:10 
@Brief   : 
"""
from abc import ABC
from collections import MutableMapping


class MapBase(MutableMapping, ABC):
    """Our own abstract data class that includes a nonpublic _Item class."""

    class _Item:
        """Lightweight composite to store key-value pairs as map items."""

        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        @property
        def key(self):
            return self._key

        @property
        def value(self):
            return self._value

        def __eq__(self, other):
            return self._key == other.key

        def __ne__(self, other):
            return not(self == other)

        def __lt__(self, other):
            return self._key < other.key


class UnsortedTableMap(MapBase, ABC):
    """Map implementation using an unsorted list."""

    def __init__(self):
        """Create an empty map."""
        self._table = []

    def __getitem__(self, k):
        """Return value associated with key k (raise error if not found.)."""
        for item in self._table:
            if k == item.key:
                return item.value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, key, value):
        """Assign value to key, overwriting existing value if present."""
        for item in self._table:
            if key == item.key:
                item.value = value
                return
        self._table.append(self._Item(key, value))

    def __delitem__(self, key):
        """Remove item associated with key."""
        for i in range(len(self._table)):
            if key == self._table[i].key:
                self._table.pop(i)
                return
        raise KeyError('Key Error: ' + repr(key))

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item.key

