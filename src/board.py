class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[Cell.Empty for j in range(size)] for i in range(size)]

    def __str__(self):
        s: str = ""

        for j in range(self.size):
            for i in range(self.size - 1):
                s += str(self.grid[i][j]) + ' '
            s += str(self.grid[self.size - 1][j]) + '\n'

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
