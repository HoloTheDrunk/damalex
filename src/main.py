from checker import *


def main():
    checker: Checker = Checker(size=int(input("Size: ")), lines=int(input("Lines: ")))
    print(checker)

    print("Add:")
    checker.board.set(int(input("X: ")), int(input("Y: ")), int(input("Value: ")))

    print("Pawn to check's position:")
    checkedPawn = (int(input("X: ")), int(input("Y: ")))

    if checker.board.get(checkedPawn[0], checkedPawn[1]) < 0:
        checker.player = -1
    print(checker.get_all_moves(checkedPawn[0], checkedPawn[1]))


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

if __name__ == '__main__':
    main()
