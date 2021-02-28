import io
import unittest.mock
from typing import List

from homework.hw1.task2.wc import wc
from tests.hw1.task2.paths_constants import *


class WcTestCase(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(self, file_names: List[str], expected_output, mock_stdout):
        wc(file_names)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_should_not_find_file(self):
        expected_output = "No such file\n"
        self.assert_stdout([os.path.join(RESOURCES_PATH, "file_that_do_not_exist")], expected_output)

    def test_should_print_info_about_one_file(self):
        expected_output = f"1 3 5 {os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)}\n"
        self.assert_stdout([os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)], expected_output)

    def test_should_print_info_about_two_file(self):
        expected_file1_info = f"1 3 5 {os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)}"
        expected_file2_info = f"5 6 12 {os.path.join(RESOURCES_PATH, TEST_SHORT_FILE2_NAME)}"
        expected_total_info = f"6 9 17 total"
        expected_output = f"{expected_file1_info}\n{expected_file2_info}\n{expected_total_info}\n"
        file1_path = os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)
        file2_path = os.path.join(RESOURCES_PATH, TEST_SHORT_FILE2_NAME)
        self.assert_stdout([file1_path, file2_path], expected_output)
