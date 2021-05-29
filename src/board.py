from typing import *

from colours import *


class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[Cell.Empty for j in range(size)] for i in range(size)]

    def __str__(self):
        s: str = "ji"

        for i in range(self.size):
            s += str(i) + '  '
        s += '\n'
        for j in range(self.size):
            s += str(j)
            for i in range(self.size - 1):
                if self.grid[i][j] > 0:
                    s += Colour.WHITE
                elif self.grid[i][j] < 0:
                    s += Colour.BLACK
                else:
                    s += Colour.RESET
                s += (' ' if self.grid[i][j] >= 0 else '') + str(self.grid[i][j]) + ' ' + Colour.RESET
            if self.grid[self.size - 1][j] > 0:
                s += Colour.WHITE
            elif self.grid[self.size - 1][j] < 0:
                s += Colour.BLACK
            else:
                s += Colour.RESET
            s += (' ' if self.grid[self.size - 1][j] >= 0 else '') + str(self.grid[self.size - 1][j]) + '\n'

        return s

    def get(self, x: int, y: int):
        return self.grid[x][y]

    def set(self, x: int, y: int, v: int):
        self.grid[x][y] = v


class Cell:
    Empty = 0

    White = 1
    WhiteQueen = 2

    Black = -1
    BlackQueen = -2
