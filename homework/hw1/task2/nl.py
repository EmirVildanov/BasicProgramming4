import sys


def nl(file_name: str):
    count = 1
    try:
        with open(file_name, "r") as f:
            for line in f:
                if line == "\n":
                    continue
                print(f"{count} {line.rstrip()}",)
                count += 1
    except FileNotFoundError:
        print("No such file")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        nl(sys.argv[1])
    elif len(sys.argv) > 2:
        print("Too many arguments")
    else:
        print("Specify the path to the file")