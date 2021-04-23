import random
from multiprocessing import Process
from multiprocessing import Pipe


def quicksort(numbers_list):
    if len(numbers_list) <= 1:
        return numbers_list
    pivot = numbers_list.pop(random.randint(0, len(numbers_list) - 1))

    return (
        quicksort([x for x in numbers_list if x < pivot]) + [pivot] + quicksort([x for x in numbers_list if x >= pivot])
    )


def process_quicksort(numbers_list, conn, procNum):

    if procNum <= 0 or len(numbers_list) <= 1:
        conn.send(quicksort(numbers_list))
        conn.close()
        return

    pivot = numbers_list.pop(random.randint(0, len(numbers_list) - 1))

    leftSide = [x for x in numbers_list if x < pivot]
    rightSide = [x for x in numbers_list if x >= pivot]

    pconnLeft, cconnLeft = Pipe()
    leftProc = Process(target=process_quicksort, args=(leftSide, cconnLeft, procNum - 1))

    pconnRight, cconnRight = Pipe()
    rightProc = Process(target=process_quicksort, args=(rightSide, cconnRight, procNum - 1))

    leftProc.start()
    rightProc.start()

    conn.send(pconnLeft.recv() + [pivot] + pconnRight.recv())
    conn.close()

    leftProc.join()
    rightProc.join()


def get_sorted_numbers_list(numbers):
    pconn, cconn = Pipe()
    p = Process(target=process_quicksort, args=(numbers, cconn, 3))
    p.start()
    numbers = pconn.recv()
    p.join()
    return numbers


if __name__ == "__main__":
    numbers = [1, 3, 6, 9, 1, 2, 3, 8, 6]
    print(get_sorted_numbers_list(numbers))
