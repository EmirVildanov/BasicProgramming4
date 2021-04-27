import time
import unittest
from datetime import datetime
from random import randint
from threading import Thread
from typing import List

from homework.hw6.semaphore import Semaphore
from tests.utils import extract_message_string_from_context


class SemaphoreTestCase(unittest.TestCase):
    def test_should_throw_error_when_trying_to_create_semaphore_with_wrong_arguments(self):
        with self.assertRaises(ValueError) as context:
            sem = Semaphore(3, 5)

        self.assertTrue(
            "[captured_number] parameter can not be bigger than [threads_max_number] parameter"
            in extract_message_string_from_context(context)
        )

    def test_should_pass_only_one_thread_in_critical_section(self):
        def function(sem: Semaphore):
            with sem:
                time.sleep(0.5)

        start_time = datetime.now()
        semaphore = Semaphore(1)
        threads = []
        for i in range(10):
            t = Thread(target=function, args=(semaphore,))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()
        self.assertTrue((datetime.now() - start_time).seconds >= 5)

    def test_should_fill_array_with_first_three_threads_value(self):
        def function(sem: Semaphore, array: List, value: int):
            with sem:
                array.append(value)
                time.sleep(randint(5, 10) / 10)

        array = []
        semaphore = Semaphore(3)
        threads = []
        for i in range(10):
            t = Thread(target=function, args=(semaphore, array, i))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()
        self.assertEqual([0, 1, 2], array[:3])

    def test_should_check_semaphore_without_context_manager(self):
        def function(sem: Semaphore, array: List, value: int):
            try:
                sem.acquire()
                if value == 0 or value == 1 or value == 2:
                    raise ValueError
                array.append(value)
                time.sleep(randint(5, 10) / 10)
            except ValueError:
                pass
            finally:
                sem.release()

        array = []
        semaphore = Semaphore(3)
        threads = []
        for i in range(6):
            t = Thread(target=function, args=(semaphore, array, i))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()
        self.assertEqual([3, 4, 5], array[:3])
        print(array)

    def test_should_check_semaphore_works_with_passed_captured_number_argument(self):
        def function(sem: Semaphore):
            with sem:
                time.sleep(0.25)

        def free_semaphore(sem: Semaphore):
            time.sleep(4)
            sem.release()

        start_time = datetime.now()
        semaphore = Semaphore(1, 1)
        threads = []
        for i in range(4):
            t = Thread(target=function, args=(semaphore,))
            threads.append(t)
            t.start()
        Thread(target=free_semaphore, args=(semaphore,)).start()
        for thread in threads:
            thread.join()
        self.assertTrue((datetime.now() - start_time).seconds >= 5)


if __name__ == "__main__":
    unittest.main()
