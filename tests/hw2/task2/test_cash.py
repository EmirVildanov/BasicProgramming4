import unittest.mock

from homework.hw2.task2.cash_decorator import cash


class CashTestCase(unittest.TestCase):
    def test_should_find_sum_result_with_cash_decorator(self):
        @cash(n=3)
        def custom_sum(a: int, b: int):
            return a + b

        self.assertEqual(3, custom_sum(1, 2))

    def test_should_cash_result_of_sum_function(self):
        @cash(n=3)
        def custom_sum(a: int, b: int):
            return a + b

        for i in range(3):
            custom_sum(1, 2)
        self.assertEqual(1, custom_sum.function_called_number)

    def test_should_not_cash_result_of_sum_function(self):
        @cash()
        def custom_sum(a: int, b: int):
            return a + b

        for i in range(3):
            custom_sum(1, 2)
        self.assertEqual(3, custom_sum.function_called_number)

    def test_should_not_cash_result_of_sum_function_with_non_braces_decorator_usage(self):
        @cash
        def custom_sum(a: int, b: int):
            return a + b

        for i in range(3):
            custom_sum(1, 2)
        self.assertEqual(3, custom_sum.function_called_number)

    def test_should_cash_result_of_function_with_args(self):
        @cash(n=3)
        def custom_sum(a: int, b: int, *args: int):
            return sum([a, b, *args])

        for i in range(3):
            custom_sum(1, 2, 3, 4)
        self.assertEqual(1, custom_sum.function_called_number)

    def test_should_cash_result_of_function_with_kwargs(self):
        @cash(n=3)
        def custom_sum(a: int, b: int, **kwargs):
            return sum([a, b, *kwargs.values()])

        for i in range(3):
            custom_sum(1, 2, c=4, d=5)
        self.assertEqual(1, custom_sum.function_called_number)

    def test_should_cash_result_of_function_with_kwargs_that_values_contains_object_of_custom_class(self):
        class CustomClass:
            def __init__(self, val1: int):
                self.val1 = val1

        @cash(n=3)
        def custom_sum(a: int, b: int, **kwargs):
            return sum([a, b])

        for i in range(3):
            custom_sum(1, 2, c=4, d=CustomClass(1))
        for item in custom_sum.cash:
            print(item)
        self.assertEqual(1, custom_sum.function_called_number)

    def test_should_cash_result_of_function_with_both_args_and_kwargs(self):
        @cash(n=3)
        def custom_sum(a: int, b: int, *args: int, **kwargs):
            return sum([a, b, *args, *kwargs.values()])

        for i in range(3):
            custom_sum(1, 2, c=4, d=5)
        self.assertEqual(1, custom_sum.function_called_number)

    def test_should_not_cash_result_of_function_as_passing_different_arguments(self):
        @cash(n=3)
        def custom_sum(a: int, b: int, *args: int, **kwargs):
            return sum([a, b, *args, *kwargs.values()])

        custom_sum(1, 2, c=4, d=5)
        custom_sum(1, 1, c=4, d=5)
        custom_sum(5, 1, c=4, d=5)
        self.assertEqual(3, custom_sum.function_called_number)

    def test_should_delete_value_from_cash(self):
        @cash(n=3)
        def custom_sum(a: int, b: int, *args: int, **kwargs):
            return sum([a, b, *args, *kwargs.values()])

        custom_sum(1, 2, c=4, d=5)
        custom_sum(1, 1, c=4, d=5)
        custom_sum(5, 1, c=4, d=5)
        custom_sum(5, 1, c=42, d=5)
        custom_sum(1, 2, c=4, d=5)
        self.assertEqual(4, custom_sum.function_called_number)
