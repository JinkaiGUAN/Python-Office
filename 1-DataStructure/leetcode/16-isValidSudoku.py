# -*- coding: UTF-8 -*-
"""
@Project : leetcode 
@File    : 16-isValidSudoku.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 04/12/2021 09:32 
@Brief   : 
"""
from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        def transfer_list(strs: List[str]) -> List[str]:
            return list(''.join(strs).replace('.', ''))

        # Check row of the board
        for row in board:
            new_strs = transfer_list(row)
            if len(set(new_strs)) != len(new_strs):
                return False

        # Check column of the board
        for i in range(len(board[0])):
            column_strs = transfer_list([s[i] for s in board])
            if len(set(column_strs)) != len(column_strs):
                return False

        # Check the window
        for i in range(3):
            # controls the row axis
            index_i = i * 3

            for j in range(3):
                # control the column axis
                index_j = j * 3
                # Note: Here we do not need to think about the IndexError problem, since IndexError can occur when we
                # retrieve a certain value, while if we slice a list, it would noy and return a blank list instead
                slide_window = [row[index_j: (j + 1) * 3] for row in board[index_i: (i + 1) * 3]]
                square_strs = transfer_list([''.join(row) for row in slide_window])
                if len(set(square_strs)) != len(square_strs):
                    return False

        return True


if __name__ == '__main__':
    board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
             ["6", ".", ".", "1", "9", "5", ".", ".", "."],
             [".", "9", "8", ".", ".", ".", ".", "6", "."],
             ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
             ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
             ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
             [".", "6", ".", ".", ".", ".", "2", "8", "."],
             [".", ".", ".", "4", "1", "9", ".", ".", "5"],
             [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
    print(Solution().isValidSudoku(board))
