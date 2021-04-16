import time
import unittest
from threading import Thread

from homework.hw6.semaphore import Semaphore
import multiprocessing as mp


class SemaphoreTestCase(unittest.TestCase):
    def test_should_pass_only_two_threads_in_shared_space(self):
        semaphore = Semaphore(1)

        def thread_fun(index):
            # if index == 0 or index == 1:
            #     time.sleep(3000)
            # for i in range(index * 10, (index + 1) * 10):
            #     array.append(i)
            with semaphore:
                if index == 0 or index == 1:
                    time.sleep(3000)
                for i in range(index * 10, (index + 1) * 10):
                    array.append(i)

        array = []
        threads = []
        for i in range(10):
            threads.append(Thread(target=thread_fun, args=(i,)))
        for thread in threads:
            thread.start()
        print(array)
        # self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
