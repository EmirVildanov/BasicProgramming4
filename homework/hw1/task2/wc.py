import sys
from typing import List


def wc(file_names: List[str]):
    total_lines, total_words, total_bytes = 0, 0, 0
    for filepath in file_names:
        current_file_lines, current_file_words, current_file_bytes = 0, 0, 0
        try:
            with open(filepath) as f:
                for line in f:
                    current_file_lines += 1
                    current_file_words += len(line.split())
                    current_file_bytes += len(bytes(line, encoding="utf8"))
            total_lines += current_file_lines
            total_words += current_file_words
            total_bytes += current_file_bytes
            print(
                f"{current_file_lines}\t{current_file_words}\t{current_file_bytes}\t{filepath}"
            )
        except FileNotFoundError:
            print(f"No such file {filepath}")
    if len(file_names) > 1:
        print(f"{total_lines}\t{total_words}\t{total_bytes}\ttotal")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        wc(sys.argv[1:])
    else:
        print("Specify the path to the file")
