from board import *
from player import *


# TODO:
#   Rules:
#       - Pawn eating
#       - Queen movement check
#       - Queen eating
#       - Mandatory eating check


def filter_moves(moves) -> None:
    """
    Remove moves that aren't jumps if any jump is possible.
    :param moves: List of possible move
    :type moves: List[(int, int, bool)]
    """
    jumps = [m for m in moves if m[2]]

    if len(jumps) != 0:
        moves.clear()
        moves += jumps

    return


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

    def get_edible_in_direction(self, startX: int, startY: int, normOffset: (int, int)) \
            -> (tuple[int, int], list[tuple[int, int]]):
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

        i: int = 0
        j: int = 0

        # If there is at least one cell after the current point in the diagonal...
        while self.contains(startX + i + normOffset[0], startY + j + normOffset[1]):
            cell: int = self.board.get(startX + i, startY + j)
            # ...and if the current point in the diagonal contains an enemy...
            if cell == -self.player or cell == -2 * self.player:
                # ...return the enemy's position as well as the empty cells after it (can be an empty list).
                return ((startX + i, startY + j),
                        (self.get_empty_diagonal(startX + i + normOffset[0],
                                                 startY + j + normOffset[1],
                                                 normOffset)))
            i += normOffset[0]
            j += normOffset[1]
        # If no enemy with empty space following it was found, return the empty space before
        # the first enemy encountered (if there was one, empty cells can be an empty list here too).
        return (-1, -1), self.get_empty_diagonal(startX + normOffset[0], startY + normOffset[1], normOffset)

    def get_empty_diagonal(self, x: int, y: int, normOffset: (int, int)) -> List[tuple[int, int]]:
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
        while self.contains(x, y) and self.board.get(x, y) == Cell.Empty:
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

        if abs(current) == 1:
            self.check_for_pawn(x, y, moves)
            print("Pawn!")
        elif abs(current) == 2:
            print("Queen!")
            self.check_for_queen(x, y, moves)

        filter_moves(moves)

        return moves

    def check_for_pawn(self, x: int, y: int, moves):
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

    def check_for_queen(self, x: int, y: int, moves) -> None:
        """
        Finds all the possible moves for a queen.
        :param x: x position of the queen to check for
        :param y: y position of the queen to check for
        :param moves: empty list that will be filled with possible moves
        :type moves: List[(int, int, bool)]
        """
        # check basic move (no jump)
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                empty_diagonal = self.get_empty_diagonal(x + i, y + j, (i, j))
                simple_moves = list((e[0], e[1], False) for e in empty_diagonal)
                moves += simple_moves

                edible_diagonal = self.get_edible_in_direction(x + i, y + j, (i, j))
                jump_moves = []
                if edible_diagonal[0][0] != -1:
                    jump_moves = list((pos[0], pos[1], True) for pos in edible_diagonal[1])
                moves += jump_moves
                print(
                    f"==Offset({i},{j}) ==> {empty_diagonal} | {edible_diagonal[1]} ==> {simple_moves} | {jump_moves}")
        return

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
        return 0 <= x < self.board.size and 0 <= y < self.board.size

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
