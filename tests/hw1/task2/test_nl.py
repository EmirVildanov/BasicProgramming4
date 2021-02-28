import io
import unittest.mock

from homework.hw1.task2.nl import nl
from tests.hw1.task2.paths_constants import *


class NlTestCase(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(self, file_name: str, expected_output, mock_stdout):
        nl(file_name)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_should_not_find_file(self):
        expected_output = "No such file\n"
        self.assert_stdout(os.path.join(RESOURCES_PATH, "file_that_do_not_exist"), expected_output)

    def test_should_print_1_nl_lines(self):
        expected_output = "1 a b c\n"
        self.assert_stdout(os.path.join(RESOURCES_PATH, TEST_SHORT_FILE1_NAME), expected_output)

    def test_should_print_4_nl_lines(self):
        expected_output = "1 d\n2 e\n3 f g h\n4 i\n"
        self.assert_stdout(os.path.join(RESOURCES_PATH, TEST_SHORT_FILE2_NAME), expected_output)

    def test_should_print_3_nl_lines(self):
        expected_output = "1 word1 word2 word3\n2 word4\n3 word7\n"
        self.assert_stdout(os.path.join(RESOURCES_PATH, TEST_FILE_WITH_BLANK_LINES_NAME), expected_output)
