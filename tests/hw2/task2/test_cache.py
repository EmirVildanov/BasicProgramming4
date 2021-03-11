import unittest.mock

from homework.hw2.task2.cache_decorator import FunctionWithCache


class CacheTestCase(unittest.TestCase):
    def test_should_find_sum_result_with_cache_decorator(self):
        @FunctionWithCache(cache_size=3)
        def custom_sum(a: int, b: int):
            return a + b

        self.assertEqual(3, custom_sum(1, 2))

    def test_should_cache_result_of_sum_function(self):
        @FunctionWithCache(cache_size=3)
        def custom_sum(a: int, b: int):
            return a + b

        for i in range(3):
            custom_sum(1, 2)
        self.assertEqual(1, custom_sum._function_called_number)

    def test_should_not_cache_result_of_sum_function(self):
        @FunctionWithCache()
        def custom_sum(a: int, b: int):
            return a + b

        for i in range(3):
            custom_sum(1, 2)
        self.assertEqual(3, custom_sum._function_called_number)

    def test_should_not_cache_result_of_sum_function_with_non_braces_decorator_usage(self):
        @FunctionWithCache
        def custom_sum(a: int, b: int):
            return a + b

        for i in range(3):
            custom_sum(1, 2)
        self.assertEqual(3, custom_sum._function_called_number)

    def test_should_cache_result_of_function_with_args(self):
        @FunctionWithCache(cache_size=3)
        def custom_sum(a: int, b: int, *args: int):
            return sum([a, b, *args])

        for i in range(3):
            custom_sum(1, 2, 3, 4)
        self.assertEqual(1, custom_sum._function_called_number)

    def test_should_cache_result_of_function_with_kwargs(self):
        @FunctionWithCache(cache_size=3)
        def custom_sum(a: int, b: int, **kwargs):
            return sum([a, b, *kwargs.values()])

        for i in range(3):
            custom_sum(1, 2, c=4, d=5)
        self.assertEqual(1, custom_sum._function_called_number)

    def test_should_cache_result_of_function_with_both_args_and_kwargs(self):
        @FunctionWithCache(cache_size=3)
        def custom_sum(a: int, b: int, *args: int, **kwargs):
            return sum([a, b, *args, *kwargs.values()])

        for i in range(3):
            custom_sum(1, 2, c=4, d=5)
        self.assertEqual(1, custom_sum._function_called_number)

    def test_should_not_cache_result_of_function_as_passing_different_arguments(self):
        @FunctionWithCache(cache_size=3)
        def custom_sum(a: int, b: int, *args: int, **kwargs):
            return sum([a, b, *args, *kwargs.values()])

        custom_sum(1, 2, c=4, d=5)
        custom_sum(1, 1, c=4, d=5)
        custom_sum(5, 1, c=4, d=5)
        self.assertEqual(3, custom_sum._function_called_number)

    def test_should_delete_value_from_cache(self):
        @FunctionWithCache(cache_size=3)
        def custom_sum(a: int, b: int, *args: int, **kwargs):
            return sum([a, b, *args, *kwargs.values()])

        custom_sum(1, 2, c=4, d=5)
        custom_sum(1, 1, c=4, d=5)
        custom_sum(5, 1, c=4, d=5)
        custom_sum(5, 1, c=42, d=5)
        custom_sum(1, 2, c=4, d=5)
        self.assertEqual(4, custom_sum._function_called_number)

    def test_should_check_that_function_under_wrapper_saves_its_info(self):
        def custom_sum(a: int, b: int, *args: int, **kwargs):
            return sum([a, b, *args, *kwargs.values()])

        decorated_custom_sum = FunctionWithCache(custom_sum, 3)
        self.assertEqual(decorated_custom_sum.__name__, custom_sum.__name__)
        self.assertEqual(decorated_custom_sum.__doc__, custom_sum.__doc__)
        self.assertEqual(decorated_custom_sum.__module__, custom_sum.__module__)
