class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[Cell.Empty for j in range(size)] for i in range(size)]

    def __str__(self):
        s: str = ""

        for j in range(self.size - 1):
            for i in range(self.size - 1):
                s += ''.join(self.grid[i][j], ' ')
            s += ''.join(self.grid[self.size - 1][j], '\n')
        s += self.grid[self.size - 1][self.size - 1]

        print(s)
        return


class Cell:
    Empty = 0
    White = 1
    Black = -1
