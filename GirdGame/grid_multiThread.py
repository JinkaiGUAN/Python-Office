# -*- coding: UTF-8 -*-
"""
@Project : ConcurrencyAndParallelism 
@File    : grid_multiThread.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 06/12/2021 09:15 
@Brief   : 
"""
import time

"""
We are going to achieve this kind of layout of the grid.
ALIVE = '*'
EMPTY = '-'

 0 | 1 | 2 | 3 | 4 
----- | ----- | ----- | ----- | -----
-*--- | --*-- | --**- | --*-- | -----
--**- | --**- | -*--- | -*--- | -**--
---*- | --**- | --**- | --*-- | -----
----- | ----- | ----- | ----- | -----
"""
import typing as t
from threading import Lock, Thread

ALIVE = '*'
EMPTY = '-'


class Grid:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.rows = [[EMPTY] * self.width for _ in range(self.height)]

    def get(self, y: int, x: int) -> str:
        """Get the status of the corresponding coordinates.

        Args:
            y (int): The y coordinate of the marker.
            x (int): The x coordinate of the marker.

        Returns:
            str: - or *.
        """
        return self.rows[y % self.height][x % self.width]

    def set(self, y: int, x: int, state: str) -> None:
        """Set the corresponding coordinates to the state we want.

        Args:
            y (int): The y coordinate of the marker.
            x (int): The x coordinate of the marker.
            state (str): - or *.11

        Returns:

        """
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        """Using `print`` function to plot the grid representation.

        Returns:

        """
        return '\n'.join([''.join(row) for row in self.rows])


class LockingGrid(Grid):
    def __init__(self, height: int, width: int) -> None:
        super(LockingGrid, self).__init__(height, width)
        self.lock = Lock()

    def __str__(self) -> str:
        with self.lock:
            return super().__str__()

    def get(self, y: int, x: int) -> str:
        with self.lock:
            return super(LockingGrid, self).get(y, x)

    def set(self, y: int, x: int, state: str) -> None:
        with self.lock:
            return super(LockingGrid, self).set(y, x, state)


def count_neighbours(y: int, x: int, get: t.Callable) -> int:
    """Retrieve the status of neighboring cells.

    Args:
        y ():
        x ():
        get ():

    Returns:

    """
    n_ = get(y - 1, x + 0)  # North
    ne = get(y - 1, x + 1)  # Northeast
    e_ = get(y + 0, x + 1)  # East
    se = get(y + 1, x + 1)  # Southeast
    s_ = get(y + 1, x + 0)  # South
    sw = get(y + 1, x - 1)  # Southwest
    w_ = get(y + 0, x - 1)  # West
    nw = get(y - 1, x - 1)  # Northwest
    neighbour_states =  [n_, ne, e_, se, s_, sw, w_, nw]

    count = 0
    for state in neighbour_states:
        if state == ALIVE:
            count += 1

    return count


def game_logic(state: str, neighbours: int) -> str:
    """Define the simple logic for the game:
    Die if a cell has fewer than two neighbors, die if a cell has more than three neighbors, or become alive if an
    empty cell has exactly three neighbors.

    Args:
        state ():
        neighbours ():

    Returns:

    """
    if state == ALIVE:
        if neighbours < 2:
            return EMPTY
        elif neighbours > 3:
            time.sleep(0.1)
            return EMPTY
    else:
        if neighbours == 3:
            return ALIVE

    return state


def step_cell(y, x, get: t.Callable, set_: t.Callable) -> None:
    state = get(y, x)
    neighbors = count_neighbours(y, x, get)
    next_state = game_logic(state, neighbors)
    set_(y, x, next_state)


def simulate_thread(grid: Grid) -> Grid:
    next_grid = LockingGrid(grid.height, grid.width)

    threads = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            thread = Thread(target=step_cell, args=args)
            thread.start()  # Fan out
            threads.append(thread)

    for thread in threads:
        thread.join()  # Fan in

    return next_grid


class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def _retrieve_infor(self):
        if self.columns:
            grid_repr = self.columns[0].split('\n')
            self.height, self.width = len(grid_repr), len(grid_repr[0])

    def __str__(self):
        if not columns:
            raise Exception(f'No items in the {self.__class__.__name__} instance.')

        # Retrieve height and width of the grid object.
        self._retrieve_infor()

        # Create the the header of multiple grid
        format_str = '{' + f':^{self.width}' + '}'
        header = ' | '.join([format_str.format(i) for i in range(len(self.columns))])

        # split the grid string into a list for all columns and store them in a dictionary. The key represents the
        # order of the column.
        grid_represent = {i: column.split('\n') for i, column in enumerate(self.columns)}

        # Merge the grid column by column
        res = ''
        for row in range(self.height):
            # Retrieve the row-th representation of all column, store them in a list
            row_str = [grid_represent.get(col)[row] for col in range(len(grid_represent))]
            res += ' | '.join(row_str) + '\n'

        return header + '\n' + res

    def append(self, column: Grid) -> None:
        self.columns.append(str(column))


if __name__ == '__main__':
    grid = LockingGrid(5, 9)
    grid.set(0, 3, ALIVE)
    grid.set(1, 4, ALIVE)
    grid.set(2, 2, ALIVE)
    grid.set(2, 3, ALIVE)
    grid.set(2, 4, ALIVE)
    print(str(grid))

    columns = ColumnPrinter()
    for _ in range(5):
        columns.append(grid)
        grid = simulate_thread(grid)

    print(columns)

