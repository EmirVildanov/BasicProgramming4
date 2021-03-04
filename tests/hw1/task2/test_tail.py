import io
import unittest.mock

from homework.hw1.task2.tail import tail
from tests.hw1.task2.paths_constants import *


class TailTestCase(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(self, file_name: str, n: int, expected_output: str, mock_stdout: io.StringIO):
        tail(file_name, n)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_should_not_find_file(self):
        file_name = "file_that_does_not_exist"
        expected_output = f"No such file {os.path.join(RESOURCES_PATH, file_name)}\n"
        self.assert_stdout(os.path.join(RESOURCES_PATH, file_name), 10, expected_output)

    def test_should_print_4_last_names(self):
        expected_output = "Tripura\nUttar Pradesh\nUttarakhand\nWest Bengal\n"
        self.assert_stdout(os.path.join(RESOURCES_PATH, TEST_FILE_WITH_NAMES_NAME), 4, expected_output)

    def test_should_print_3_last_lines(self):
        expected_output = "f g h\n\ni\n"
        self.assert_stdout(os.path.join(RESOURCES_PATH, TEST_SHORT_FILE2_NAME), 3, expected_output)
