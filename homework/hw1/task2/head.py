import sys


def head(file_name: str, n: int = 10):
    try:
        with open(file_name, "r") as f:
            for i, line in enumerate(f):
                if i == n:
                    break
                print(line.rstrip())
    except FileNotFoundError:
        print("No such file")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        head(sys.argv[1])
    elif len(sys.argv) == 3:
        second_argument = sys.argv[2]
        if second_argument.isdigit():
            head(sys.argv[1], int(second_argument))
        else:
            print("Second argument is not int")
    elif len(sys.argv) > 3:
        print("Too many arguments")
    else:
        print("Specify the path to the file")
