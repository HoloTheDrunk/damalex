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
        self.players: Player = Player(size * 2)

        self.turn: int = 0
        self.player: int = 0

    def __str__(self):
        return str(self.board)

    def play(self, x: int, y: int):
        self.board.set(x, y, self.turn)
        self.turn = 1 - self.turn

    def move(self, x: int, y: int, goalX: int, goalY: int, player: int):
        # Receive player as 0/1 value, change to -1/1
        player = 2 * player - 1

        # Check if move is valid
        check: int = self.check_move(x, y, goalX, goalY, player)

        # Invalid move
        if check == -1:
            return Move.Invalid

        # "Move" piece
        self.board.set(goalX, goalY, self.board.get(x, y))
        self.board.set(x, y, Cell.Empty)

        # Only takes pawns into account for now
        if check == 4:
            self.jump(x, y, goalX, goalY)
            return Move.Jumped

        return Move.Moved

    def check_move(self, startX: int, startY: int, goalX: int, goalY: int, player: int):
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

    def check_diagonal_for_enemies(self, startX: int, startY: int, goalX: int, goalY: int, player: int):
        player: int = player * 2 - 1
        offset: (int, int) = (goalX - startX, goalY - startY)

        for i in range(abs(goalX - startX)):
            if (self.board.get(startX + offset[0], startY + offset[1]) == -player
                    or self.board.get(startX + i, startY + i) == -2 * player):
                return True

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
