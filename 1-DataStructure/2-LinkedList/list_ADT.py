from positional_list_ADT import Position, PositionalList


class Item:
    def __init__(self, value) -> None:
        self.value = value 
        self.count = 0


class FavoriteList:

    def __init__(self) -> None:
        self.data = PositionalList()

    def __len__(self):
        return len(self.data)

    def is_empty(self):
        return len(self.data) == 0

    def _find_position(self, value):
        """Search for element value and eturn its Position (or None if not found)."""
        walk = self.data.first()
        while walk is not None and walk.value() != value:
            walk = self.data.after(walk)
        return walk

    def _move_up(self, p: Position):
        """Move item at Position p earlier in the list based on access count."""
        if p != self.data.first():
            cnt = p.element().count 
            walk = self.data.before(p)
            if cnt > walk.element().count:
                while (walk != self.data.first() and cnt > self.data.before(walk).element().count):
                    walk = self.data.before(walk)
                self.data.add_before(walk, self.data.delete(p))

    def access(self, value):
        """Access element value, thereby increaing its access count."""
        p = self._find_position(value)
        if p is None:
            p = self.data.add_last(Item(value))
        p.element().count += 1
        self._move_up(p)

    def remove(self, value):
        """"Remove element value from the list of favorites."""
        p = self._find_position(value)
        if not p:
            self.data.delete(p)

    def top(self, k: int):
        """Generate sequence of top k elements in terms of access count."""
        if not 1 <= k <= len(self):
            raise ValueError('Illegal valur for k')
        walk = self.data.first()
        for j in range(k):
            item = walk.element()
            yield item.value
            walk = self.data.after(walk)

