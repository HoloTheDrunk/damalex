from checker import *


def main():
    checker: Checker = Checker(size=10, lines=4)
    print("Initial board=================")
    pprint_board(checker.board, [])

    adding: bool = True
    while adding:
        print("Set(x, y, value)==============")
        checker.board.set(int(input("X: ")), int(input("Y: ")), int(input("Value: ")))

        adding = input("Add another ? (y/n)").lower() == 'y'

    print("Piece move check===============")
    checkedPiece = (int(input("X: ")), int(input("Y: ")))

    if checker.board.get(checkedPiece[0], checkedPiece[1]) < 0:
        checker.player = -1
    possibleMoves = checker.get_all_moves(checkedPiece[0], checkedPiece[1])

    print("Possible moves================\n" + str(possibleMoves))
    print("Board=========================")
    pprint_board(checker.board, possibleMoves)

    print("Filtering moves===============\n")
    filter_moves(possibleMoves)
    print(possibleMoves)
    print("Board=========================")
    pprint_board(checker.board, possibleMoves)

    # TODO:
    #   - GUI !!!!!!
    #   - Logic:
    #       - Get input
    #       - Store playable moves
    #       - Get input
    #       - Check playable moves
    #       - Move
    #   - Game:
    #       - Queen move check
    #       - AI


def pprint_board(board: Board, possibleMoves: [(int, int, bool)]):
    s: str = Colour.UI + "  "

    for i in range(board.size):
        s += str(i) + '  '
    s += '\n'
    for j in range(board.size):
        s += Colour.UI + str(j) + Colour.RESET
        for i in range(board.size - 1):
            if board.grid[i][j] > 0:
                s += Colour.WHITE
            elif board.grid[i][j] < 0:
                s += Colour.BLACK
            else:
                if (i, j, False) in possibleMoves or (i, j, True) in possibleMoves:
                    s += Colour.VALID
                else:
                    s += Colour.RESET
            s += (' ' if board.grid[i][j] >= 0 else '') + str(board.grid[i][j]) + ' ' + Colour.RESET
        if board.grid[board.size - 1][j] > 0:
            s += Colour.WHITE
        elif board.grid[board.size - 1][j] < 0:
            s += Colour.BLACK
        else:
            s += Colour.RESET
        s += (' ' if board.grid[board.size - 1][j] >= 0 else '') + str(
            board.grid[board.size - 1][j]) + '\n' + Colour.RESET

    print(s)


if __name__ == '__main__':
    main()
