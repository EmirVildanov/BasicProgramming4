import sys
from typing import List


def wc(file_names: List[str]):
    total_lines = 0
    total_words = 0
    total_bytes = 0
    for filepath in file_names:
        current_file_lines = 0
        current_file_words = 0
        current_file_bytes = 0
        try:
            with open(filepath) as f:
                for line in f:
                    current_file_lines += 1
                    current_file_words += len(line.split())
                    current_file_bytes += len(bytes(line, encoding="utf8"))
            total_lines += current_file_lines
            total_words += current_file_words
            total_bytes += current_file_bytes
            print(f"{current_file_lines} {current_file_words} {current_file_bytes} {filepath}")
        except FileNotFoundError:
            print("No such file")
    if len(file_names) > 1:
        print(f"{total_lines} {total_words} {total_bytes} total")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        wc(sys.argv[1:])
    else:
        print("Specify the path to the file")