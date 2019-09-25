from spider import Spider
import sys


def main(arg):
    if arg == "-h" or arg == "--help":
        print("This program crawled websites." + "\n\n" + " arguments: valid link \n example: https://anytask.org/")
    if arg == "-clear":
        clear()
    else:
        spider = Spider(arg)
        spider.go()


def clear():
    pass


if __name__ == '__main__':
    main(sys.argv[1])

