import time
from random import randint
from threading import currentThread, Lock, Thread
from homework.hw6.semaphore import Semaphore


class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = Lock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            print(f"{name} Running: {self.active}")

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            print(f"{name} Running: {self.active}")


def function(semaphore, pool):
    print(f"{currentThread().getName()} Waiting to join the pool")
    with semaphore:
        name = currentThread().getName()
        pool.make_active(name)
        random_number = randint(5, 10)
        time.sleep(random_number / 10)
        pool.make_inactive(name)


if __name__ == "__main__":
    pool = ThreadPool()
    semaphore = Semaphore(3)
    for i in range(10):
        t = Thread(target=function, name="thread_" + str(i), args=(semaphore, pool))
        t.start()
