from threading import Lock


class Semaphore:
    """
    Custom implementation of Semaphore class from threading
    """

    def __init__(self, threads_max_number: int, captured_number: int = 0):
        if captured_number > threads_max_number:
            raise ValueError("[captured_number] parameter can not be bigger than [threads_max_number] parameter")
        self._lock = Lock()
        self.threads_max_number = threads_max_number
        self.threads_free_number = threads_max_number - captured_number

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *args, **kwargs):
        self.release()

    def acquire(self):
        """
        Function that:
        passes thread in critical section if self [threads_free_number] field is bigger than 0
        makes thread wait until self [threads_free_number] field is bigger than 0
        """
        while True:
            with self._lock:
                if self.threads_free_number > 0:
                    self.threads_free_number -= 1
                    break

    def release(self):
        """
        Function that
        release thread from semaphore
        or
        do nothing if self [threads_free_number] field equals self self [threads_max_number] filed
        """
        with self._lock:
            if self.threads_free_number < self.threads_max_number:
                self.threads_free_number += 1
