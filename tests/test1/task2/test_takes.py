import unittest

from homework.test1.task2.takes import TakesFunction


class TakesTestCase(unittest.TestCase):
    def test_should_raise_exception_when_passing_parameter_of_wrong_type(self):
        @TakesFunction(int, int)
        def function(a, b):
            print(f"Successful call with a={a} and b={b}")

        with self.assertRaises(TypeError):
            function(1, "1")

    def test_should_raise_exception_when_passing_parameter_of_wrong_type_to_function_with_kwargs(self):
        @TakesFunction(int, int, int, str)
        def function_with_kwargs(a, b, **kwargs):
            print(f"Successful call with a={a} and b={b}, and kwargs={kwargs}")

        with self.assertRaises(TypeError):
            function_with_kwargs(1, 3, val1="test", val2=5)

    def test_should_not_rise_error_with_function_without_kwargs(self):
        @TakesFunction(int, int)
        def function(a, b):
            return a + b

        self.assertEqual(3, function(1, 2))

    def test_should_not_rise_error_with_function_with_kwargs(self):
        @TakesFunction(int, int, int, int)
        def function(a, b, **kwargs):
            return a + b + list(kwargs.values())[0] + list(kwargs.values())[1]

        self.assertEqual(10, function(1, 2, val1=3, val2=4))

    def test_should_not_rise_error_with_function_with_kwargs_when_decorator_has_less_arguments_than_passed_parameters(
        self,
    ):
        @TakesFunction(int, int)
        def function(a, b, **kwargs):
            return a + b + list(kwargs.values())[0] + list(kwargs.values())[1]

        self.assertEqual(10, function(1, 2, val1=3, val2=4))
