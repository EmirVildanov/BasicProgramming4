import io
import unittest.mock
from typing import List

from homework.hw1.task2.wc import wc
from tests.hw1.task2.paths_constants import *


class WcTestCase(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(self, file_names: List[str], expected_output: str, mock_stdout: io.StringIO):
        wc(file_names)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_should_not_find_file(self):
        file_name = "file_that_does_not_exist"
        expected_output = f"No such file {os.path.join(RESOURCES_PATH, file_name)}\n"
        self.assert_stdout([os.path.join(RESOURCES_PATH, file_name)], expected_output)

    def test_should_print_info_about_one_file(self):
        expected_output = f"1\t3\t5\t{os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)}\n"
        self.assert_stdout([os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)], expected_output)

    def test_should_print_info_about_two_file(self):
        expected_file1_info = f"1\t3\t5\t{os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)}"
        expected_file2_info = f"5\t6\t12\t{os.path.join(RESOURCES_PATH, TEST_SHORT_FILE2_NAME)}"
        expected_total_info = f"6\t9\t17\ttotal"
        expected_output = f"{expected_file1_info}\n{expected_file2_info}\n{expected_total_info}\n"
        file1_path = os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)
        file2_path = os.path.join(RESOURCES_PATH, TEST_SHORT_FILE2_NAME)
        self.assert_stdout([file1_path, file2_path], expected_output)
