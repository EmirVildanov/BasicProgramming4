# Реализовать семафор через менеджер контекстов (доступ к объекту через with).
# Написать тесты для него используя многопоточность.

class Semaphore:
    def __init__(self, threads_max_number: int, captured_number: int = 0):
        if captured_number > threads_max_number:
            raise ValueError("[captured_number] parameter can not be bigger than [threads_max_number] parameter")
        self.threads_max_number = threads_max_number
        self.threads_free_number = threads_max_number - captured_number

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self):
        while self.threads_free_number == 0:
            pass
        self.threads_free_number -= 1

    def release(self):
        while self.threads_free_number == self.threads_max_number:
            pass
        self.threads_free_number += 1
