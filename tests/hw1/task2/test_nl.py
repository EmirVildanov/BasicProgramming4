import io
import unittest.mock
from typing import List

from homework.hw1.task2.nl import nl
from tests.hw1.task2.paths_constants import *


class NlTestCase(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(
        self, file_names: List[str], expected_output: str, mock_stdout: io.StringIO
    ):
        nl(file_names)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_should_not_find_file(self):
        file_name = "file_that_do_not_exist"
        expected_output = f"No such file {os.path.join(RESOURCES_PATH, file_name)}\n"
        self.assert_stdout([os.path.join(RESOURCES_PATH, file_name)], expected_output)

    def test_should_print_1_nl_lines(self):
        expected_output = "1\ta b c\n"
        self.assert_stdout(
            [os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME)], expected_output
        )

    def test_should_print_4_nl_lines(self):
        expected_output = "1\td\n2\te\n3\tf g h\n4\ti\n"
        self.assert_stdout(
            [os.path.join(RESOURCES_PATH, TEST_SHORT_FILE2_NAME)], expected_output
        )

    def test_should_print_3_nl_lines(self):
        expected_output = "1\tword1 word2 word3\n2\tword4\n3\tword7\n"
        self.assert_stdout(
            [os.path.join(RESOURCES_PATH, TEST_FILE_WITH_BLANK_LINES_NAME)],
            expected_output,
        )

    def test_should_print_7_nl_lines_for_two_files(self):
        file1_expected_output = "1\tword1 word2 word3\n2\tword4\n3\tword7\n"
        file2_expected_output = "4\td\n5\te\n6\tf g h\n7\ti\n"
        expected_output = f"{file1_expected_output}{file2_expected_output}"
        self.assert_stdout(
            [
                os.path.join(RESOURCES_PATH, TEST_FILE_WITH_BLANK_LINES_NAME),
                os.path.join(RESOURCES_PATH, TEST_SHORT_FILE2_NAME),
            ],
            expected_output,
        )
