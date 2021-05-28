from checker import *


def main():
    checker: Checker = Checker(size=int(input("Size: ")), lines=int(input("Lines: ")))
    print(checker)


if __name__ == '__main__':
    main()
