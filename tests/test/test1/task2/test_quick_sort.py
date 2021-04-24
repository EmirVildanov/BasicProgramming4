import random
import unittest
from random import shuffle

from homework.tests.test1.task2.quick_sort import quicksort


class SmartArgsTestCase(unittest.TestCase):
    def test_should_check_quicksort_works_correctly1(self):
        numbers = [1, 3, 6, 9, 1, 2, 3, 8, 6]
        asserting_numbers = [1, 1, 2, 3, 3, 6, 6, 8, 9]
        result = quicksort(numbers)
        self.assertEqual(asserting_numbers, result)

    def test_should_check_quicksort_works_correctly2(self):
        asserting_numbers = [2, 5, 5, 6, 8, 32, 32, 32, 59, 90, 100, 100, 101, 200, 300]
        numbers = asserting_numbers.copy()
        shuffle(numbers)
        result = quicksort(numbers)
        self.assertEqual(asserting_numbers, result)

    def test_should_check_quicksort_works_correctly_on_big_numbers_list(self):
        asserting_numbers = list([random.randint(1, 1000) for _ in range(1000)])
        asserting_numbers.sort()
        numbers = asserting_numbers.copy()
        shuffle(numbers)
        result = quicksort(numbers)
        self.assertEqual(asserting_numbers, result)

    def test_should_check_quicksort_doing_nothing_on_sorted_list(self):
        numbers = [2, 5, 5, 6, 8, 32, 32, 32, 59, 90, 100, 100, 101, 200, 300]
        result = quicksort(numbers)
        self.assertEqual(numbers, result)


if __name__ == "__main__":
    unittest.main()
