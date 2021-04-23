import unittest

from homework.tests.test1.task2.quick_sort import get_sorted_numbers_list
from tests.utils import extract_message_string_from_context


class SmartArgsTestCase(unittest.TestCase):
    def test_should_raise_error_when_adding_instance_with_already_existed_key(self):
        with self.assertRaises(ValueError) as context:
            test = 1

        self.assertTrue(f"Test" in extract_message_string_from_context(context))

    def test_should_check_quicksort_works_correclty(self):
        numbers = [1, 3, 6, 9, 1, 2, 3, 8, 6]
        asserting_numbers = [1, 1, 2, 3, 3, 6, 6, 8, 9]
        result = get_sorted_numbers_list(numbers)
        self.assertEqual(asserting_numbers, result)


if __name__ == "__main__":
    unittest.main()
