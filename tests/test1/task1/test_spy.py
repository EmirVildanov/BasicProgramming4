import unittest.mock

from homework.test1.task1.spy import SpyFunction, print_usage_statistic


class CacheTestSpy(unittest.TestCase):
    def test_should_raise_error_when_passing_non_decorated_function(self):
        def function():
            print(1)

        with self.assertRaises(TypeError) as context:
            print_usage_statistic(function)

        self.assertTrue("Function type is not SpyFunction and it doesn't have needed fields " in str(context.exception))

    def test_should_find_sum_result_with_cache_decorator(self):
        @SpyFunction
        def custom_sum(a: int, b: int):
            return a + b

        result = custom_sum(1, 2)
        parameters_history = list()
        for _, parameters in print_usage_statistic(custom_sum):
            parameters_history += parameters
        self.assertEqual([1, 2], parameters_history)

    def test_should_return_right_parameters_of_functinon_with_kwargs(self):
        @SpyFunction
        def custom_sum(a: int, b: int, **kwargs) -> int:
            return sum(kwargs.values()) + a + b

        result = custom_sum(1, 2, val1=3, val2=4)
        parameters_history = list()
        for _, parameters in print_usage_statistic(custom_sum):
            parameters_history += parameters
        self.assertEqual([1, 2, 3, 4], parameters_history)
