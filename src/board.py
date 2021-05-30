from typing import *


class Board:
    def __init__(self, size: int, lines: int):
        if size % 2 != 0:
            raise ValueError("Board.__init__: argument 'size' should be even.")
        if lines > size / 2:
            raise ValueError("Board.__init__: argument 'lines' should be at most half of argument 'size'.")

        self.size: int = size
        self.grid: List[List[int]] = [[Cell.Empty for _ in range(size)] for _ in range(size)]

        # Initialize both sides' pawns
        for j in range(lines):
            for i in range(self.size):
                if (j + i) % 2 == 1:
                    self.grid[i][j] = Cell.Black
                else:
                    self.grid[i][self.size - (j + 1)] = Cell.White

    def get(self, x: int, y: int) -> int:
        return self.grid[x][y]

    def set(self, x: int, y: int, v: int):
        self.grid[x][y] = v


class Cell:
    Empty = 0

    White = 1
    WhiteQueen = 2

    Black = -1
    BlackQueen = -2
