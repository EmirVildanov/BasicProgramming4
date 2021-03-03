import sys
from typing import List


def nl(file_names: List[str]):
    count = 1
    for filepath in file_names:
        try:
            with open(filepath) as f:
                for line in f:
                    if line.isspace():
                        continue
                    print(
                        f"{count}\t{line.rstrip()}",
                    )
                    count += 1
        except FileNotFoundError:
            print(f"No such file {filepath}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        nl(sys.argv[1:])
    else:
        print("Specify the path to the file")
