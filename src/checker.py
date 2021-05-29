from board import *
from player import *


# TODO:
#   Rules:
#       - Pawn eating
#       - Queen movement check
#       - Queen eating
#       - Mandatory eating check


class Checker:
    def __init__(self, size: int, lines: int):
        self.board: Board = Board(size, lines)
        self.players: List[Player] = [Player(size * 2, Colour.WHITE), Player(size * 2, Colour.BLACK)]

        self.turn: int = 0
        self.player: int = 1

    def __str__(self):
        return str(self.board)

    def play(self, x: int, y: int):
        self.board.set(x, y, self.turn)
        self.turn = 1 - self.turn

    def move(self, x: int, y: int, goalX: int, goalY: int):
        """
        Move the cell at (x, y) to (goalX, goalY)
        :param x: x position of the cell to move
        :param y: y position of the cell to move
        :param goalX: x position of its new place
        :param goalY: y position of its new place
        """
        # "Move" piece
        self.board.set(goalX, goalY, self.board.get(x, y))
        self.board.set(x, y, Cell.Empty)

    def check_move(self, startX: int, startY: int, goalX: int, goalY: int):
        """
        Check if the chosen move from (startX, startY) to (goalX, goalY) is valid
        :param startX: x position of starting point
        :param startY: y position of starting point
        :param goalX: x position of ending point
        :param goalY: y position of ending point
        :return: bool
        """
        if self.contains(goalX, goalY):
            distance: int = abs(startX - goalX + startY - goalY)
            if distance == 2 and self.board.get(goalX, goalY) == Cell.Empty:
                return distance
            elif distance == 4:
                middle: int = self.board.get(startX + (1 if goalX - startX > 0 else -1),
                                             startY + (1 if goalY - startY > 0 else -1))
                if middle == -player or middle == -2 * player:
                    return distance
            # elif distance > 4 and self.board.get(startX, startY) == player*2
            #    self.board.get(startX, startY) == 2 and self.board.get(goalX, goalY) == Cell.Empty):

    def check_diagonal_for_edible(self, startX: int, startY: int, goalX: int, goalY: int):
        """
        Checks if an edible enemy is present between two cells.
        :param startX: x position of start cell
        :param startY: y position of start cell
        :param goalX: x position of goal cell
        :param goalY: y position of goal cell
        :return: Tuple containing the first enemy position
        :rtype: ((int, int), (int, int))
        """
        if not self.contains(startX, startY):
            raise ValueError("check_diagonal_for_edible: Start coordinates out of bounds.")
        if not self.contains(goalX, goalY):
            raise ValueError("check_diagonal_for_edible: Goal coordinates out of bounds.")

        offset: (int, int) = (goalX - startX, goalY - startY)
        normOffset: (int, int) = (offset[0] // abs(offset[0]), offset[1] // abs(offset[1]))

        for i in range(0, offset[0], normOffset[0]):
            for j in range(0, offset[1], normOffset[1]):
                if (self.board.get(startX + i, startY + j) == -self.player
                        or self.board.get(startX + i, startY + j) == -2 * self.player):
                    return ((startX + i, startY + j),
                            (self.get_empty_diagonal_end(startX + i + normOffset[0],
                                                         startY + j + normOffset[1],
                                                         normOffset)))
        return None, self.get_empty_diagonal_end(startX + normOffset[0], startY + normOffset[1], normOffset)

    def get_empty_diagonal_end(self, x: int, y: int, normOffset: (int, int)):
        """
        Finds the end of a diagonal of empty cells.
        :param x: x coordinate of first empty cell
        :param y: y coordinate of first empty cell
        :param normOffset: normalized direction offset
        :type normOffset: (int, int)
        :return: x and y coordinate tuple of the last empty cell or None if none are found
        :rtype: (int, int)
        """
        if self.contains(x, y) and self.board.get(x, y) == Cell.Empty:
            while (self.contains(x + normOffset[0], y + normOffset[1])
                   and self.board.get(x + normOffset[0], y + normOffset[1]) == Cell.Empty):
                x += normOffset[0]
                y += normOffset[1]
            return x, y
        return None

    def contains(self, x: int, y: int):
        return 0 < x < self.board.size and 0 < y < self.board.size

    def jump(self, x: int, y: int, goalX: int, goalY: int):
        midX: int = (x + goalX) // 2
        midY: int = (y + goalY) // 2
        self.board.set(midX, midY, Cell.Empty)


class Move:
    Jumped = 2
    Moved = 1
    Invalid = 0
