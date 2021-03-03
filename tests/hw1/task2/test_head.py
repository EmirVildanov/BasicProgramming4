import io
import unittest.mock

from homework.hw1.task2.head import head
from tests.hw1.task2.paths_constants import *


class HeadTestCase(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(
        self, file_name: str, n: int, expected_output: str, mock_stdout: io.StringIO
    ):
        head(file_name, n)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_should_not_find_file(self):
        file_name = "file_that_do_not_exist"
        expected_output = f"No such file {os.path.join(RESOURCES_PATH, file_name)}\n"
        self.assert_stdout(os.path.join(RESOURCES_PATH, file_name), 10, expected_output)

    def test_should_print_first_1_line_of_file(self):
        expected_output = "a b c\n"
        self.assert_stdout(
            os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME), 10, expected_output
        )

    def test_should_print_first_3_line_of_file(self):
        expected_output = "Andhra Pradesh\nArunachal Pradesh\nAssam\n"
        self.assert_stdout(
            os.path.join(RESOURCES_PATH, TEST_FILE_WITH_NAMES_NAME), 3, expected_output
        )
