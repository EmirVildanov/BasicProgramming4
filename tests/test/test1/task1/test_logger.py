import unittest

from homework.tests.test1.task1.logger import LoggerFunction
from tests.utils import extract_message_string_from_context


class SmartArgsTestCase(unittest.TestCase):
    def test_should_raise_error_when_calling_decorator_without_braces(self):
        with self.assertRaises(ValueError) as context:

            @LoggerFunction
            def test():
                return 1

        self.assertTrue(
            "You can not use this decorator without passing file name" in extract_message_string_from_context(context)
        )

    def test_should_raise_error_when_passing_wrong_number_of_args_in_decorator(self):
        with self.assertRaises(ValueError) as context:

            @LoggerFunction("test", 1)
            def test():
                return 1

        self.assertTrue(
            "Decorator takes only one string [save_file_path] argument" in extract_message_string_from_context(context)
        )

    def test_should_raise_error_when_passing_argument_of_wrong_type(self):
        with self.assertRaises(ValueError) as context:

            @LoggerFunction(1)
            def test():
                return 1

        self.assertTrue(
            "Decorator takes string [save_file_path] argument" in extract_message_string_from_context(context)
        )

    def test_should_check_decorator_saves_logs_into_file_that_not_exists(self):
        file_name = "save_file.txt"

        @LoggerFunction(file_name)
        def f(n, *args, **kwargs):
            if n != 0:
                f(n - 1)

        f(1, a="1", b="2")

        assert_list = [
            ["f", "(0,)", "({})", "None"],
            ["f", "(1,)", "({'a':", "'1',", "'b':", "'2'})", "None"],
        ]
        with open(file_name) as f:
            lines = f.readlines()[:-1]
            for index, line in enumerate(lines):
                info = line.split(" ")[2:-1]
                self.assertEqual(assert_list[index], info)

    def test_should_check_decorator_saves_logs_into_existing_file(self):
        file_name = "save_file2.txt"

        @LoggerFunction(file_name)
        def function_that_returns_n(n, *args, **kwargs):
            if n != 0:
                function_that_returns_n(n - 1)
            return n

        function_that_returns_n(1, a="1", b="2")

        assert_list = [
            ["function_that_returns_n", "(0,)", "({})", "0"],
            ["function_that_returns_n", "(1,)", "({'a':", "'1',", "'b':", "'2'})", "1"],
        ]
        with open(file_name) as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                info = line.split(" ")[2:-1]
                self.assertEqual(assert_list[index], info)


if __name__ == "__main__":
    unittest.main()
