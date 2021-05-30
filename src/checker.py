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

    def check_diagonal_for_edible(self, startX: int, startY: int, normOffset: (int, int)):
        """
        Checks if an edible enemy is present between two cells.
        :param startX: x position of start cell
        :param startY: y position of start cell
        :param normOffset: coordinates representing the direction of the diagonal
        :return: Tuple containing the first enemy position and position of last empty cell
        :rtype: ((int, int), List[(int, int)])
        """
        if not self.contains(startX, startY):
            raise ValueError("check_diagonal_for_edible: Start coordinates out of bounds.")

        = 2
        i: int = 0
        while
            for j in range(0, offset[1], normOffset[1]):
                if (self.board.get(startX + i, startY + j) == -self.player
                        or self.board.get(startX + i, startY + j) == -2 * self.player):
                    return ((startX + i, startY + j),
                            (self.get_empty_diagonal(startX + i + normOffset[0],
                                                     startY + j + normOffset[1],
                                                     normOffset)))
        return None, self.get_empty_diagonal(startX + normOffset[0], startY + normOffset[1], normOffset)

    def get_empty_diagonal(self, x: int, y: int, normOffset: (int, int)):
        """
        Finds the end of a diagonal of empty cells.
        :param x: x coordinate of first empty cell
        :param y: y coordinate of first empty cell
        :param normOffset: normalized direction offset
        :type normOffset: (int, int)
        :return: x and y coordinate tuple of the last empty cell or None if none are found
        :rtype: (
        """
        if abs(normOffset[0]) != 1 or abs(normOffset[1]) != 1:
            raise ValueError("get_empty_diagonal: normOffset tuple argument should have 1 or -1 in both fields.")

        retList: [(int, int)] = []
        if self.contains(x, y) and self.board.get(x, y) == Cell.Empty:
            while (self.contains(x + normOffset[0], y + normOffset[1])
                   and self.board.get(x + normOffset[0], y + normOffset[1]) == Cell.Empty):
                retList.append((x, y))
                x += normOffset[0]
                y += normOffset[1]
        return retList

    def get_all_moves(self, x: int, y: int):
        """
        Computes the list of all playable moves from a given position.
        :param x: X location of piece
        :param y: Y location of piece
        :return: Returns a list of moves as tuples containing a position and whether or not it is a jump.
        :rtype: List[(int, int, bool)]
        """
        current = self.board.get(x, y)
        moves = []

        if current == Cell.Empty:
            return moves

        if abs(current) == self.player:
            self.check_for_pawn(x, y, moves)
        elif abs(current) == 2 * self.player:
            self.check_for_queen(x, y, moves)

        self.filter_moves(moves)

        return moves

    def check_for_pawn(self, x: int, y: int, moves: List[(int, int, bool)]):
        # check basic move (no jump)
        for i in range(-1, 2, 2):
            if not self.contains(x + i, y - self.player):
                continue

            if self.board.get(x + i, y - self.player) == Cell.Empty:
                moves.append((x + i, y - self.player, False))

        # check jump move
        for i in range(-2, 3, 4):
            for j in range(-2, 3, 4):
                if not self.contains(x + i, y + j) or self.board.get(x + i, y + j) != Cell.Empty:
                    continue

                middle: int = self.board.get(x + i // 2, y + j // 2)

                if middle == -self.player or middle == -2 * self.player:
                    moves.append((x + i, y + j, True))

    def check_for_queen(self, x: int, y: int, moves: List[(int, int, bool)]):
        # check basic move (no jump)
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                moves += map(lambda e: (e[0], e[1], False), self.get_empty_diagonal(x + i, y + j, (i, j)))
                moves +=
        return

    def filter_moves(self, moves: List[(int, int, bool)], isQueen: bool):
        """
        Remove moves that should not be played according to the rule (jump priority, etc)
        :param moves: List of possible move
        :param isQueen: if the piece is a Queen or not
        """
        jump_move = [m for m in moves if True in m]
        basic_move = [m for m in moves if False in m]

        if len(jump_move) == 0:
            moves = basic_move
            return
        elif len(jump_move) == 1:
            moves = jump_move
            return

        max_path = 0
        final_path = []

        for move in jump_move:
            store_move = []
            x, y = move[0], move[1]
            possible_from = self.check_for_queen(x, y, store_move) if isQueen else self.check_for_pawn(x, y, store_move)
            possible_from.remove(move)  # not going back

            # store best jump move in store_move with all the possible_from move
            self.get_max_takes_queen(x, y, store_move, possible_from)

            if len(store_move) > max_path:
                max_path = len(store_move)
                final_path = store_move

        return store_move

    def get_max_takes_queen(self, x: int, y: int, res: List[(int, int, bool)], possible: List[(int, int, bool)]):
        """
        TODO : recursion on possible + remove current into compare as max
        :param x:
        :param y:
        :param res:
        :param possible:
        :return:
        """

    def get_max_takes_pawn(self, x: int, y: int, moves: List[(int, int, bool)]) -> None:
        visited: List[(int, int, bool)] = []
        for move in [m for m in moves if m[3]]:
            visited.append(move)
            moves.remove(move)
            if self.get_max_takes_pawn(move[0], move[1], )

    def jump_is_valid(self, start: (int, int), direction: (int, int)) -> bool:
        jump: int = self.board.get(start[0] + 2 * direction[0], start[1] + 2 * direction[1])
        if self.contains(start[0] + 2 * direction[0], start[1] + 2 * direction[1]) and jump == Cell.Empty:
            middle: int = self.board.get(start[0] + direction[0], start[1] + direction[1])
            if middle == -self.player or middle == -2 * self.player:
                return True
        return False

    def contains(self, x: int, y: int) -> bool:
        """
        Checks if the cell at (x, y) exists and is valid
        :param x: x position of the cell
        :param y: y position of the cell
        :return: Whether (x, y) exists
        """
        return 0 < x < self.board.size and 0 < y < self.board.size

    def jump(self, x: int, y: int, goalX: int, goalY: int, enemyX: int = -1, enemyY: int = -1):
        """
        Move pawn at (x, y) to (goalX, goalY), either capturing the pawn in the middle or at (enemyX, enemyY).
        :param x: x position of cell to move
        :param y: y position of cell to move
        :param goalX: new x position of cell to move
        :param goalY: new y position of cell to move
        :param enemyY: x position of eaten enemy (used for queen jumps)
        :param enemyX: y position of eaten enemy (used for queen jumps)
        """
        enemyX: int = (x + goalX) // 2 if enemyX == -1 else enemyX
        enemyY: int = (y + goalY) // 2 if enemyY == -1 else enemyY
        self.board.set(enemyX, enemyY, Cell.Empty)
        self.players[-self.player].remaining -= 1


class Move:
    Jumped = 2
    Moved = 1
    Invalid = 0
