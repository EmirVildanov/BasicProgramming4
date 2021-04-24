import random
from multiprocessing import Process
from multiprocessing import Pipe


def process_quicksort(numbers_list, conn, proc_number):
    if len(numbers_list) <= 1:
        conn.send(numbers_list)
        conn.close()
        return

    pivot = numbers_list.pop(random.randint(0, len(numbers_list) - 1))

    left_side = [x for x in numbers_list if x < pivot]
    right_side = [x for x in numbers_list if x >= pivot]

    pconn_left, cconn_left = Pipe()
    leftProc = Process(target=process_quicksort, args=(left_side, cconn_left, proc_number - 1))

    pconn_right, cconn_right = Pipe()
    rightProc = Process(target=process_quicksort, args=(right_side, cconn_right, proc_number - 1))

    leftProc.start()
    rightProc.start()

    conn.send(pconn_left.recv() + [pivot] + pconn_right.recv())
    conn.close()

    leftProc.join()
    rightProc.join()


def quicksort(numbers):
    pconn, cconn = Pipe()
    p = Process(target=process_quicksort, args=(numbers, cconn, 3))
    p.start()
    numbers = pconn.recv()
    p.join()
    return numbers
