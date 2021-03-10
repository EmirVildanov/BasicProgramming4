import unittest.mock

from homework.hw2.task1.curry import *
from tests.utils import extract_message_string_from_context


class UncurryTestCase(unittest.TestCase):
    def test_should_raise_error_when_negative_arity_is_passed_to_uncurry(self):
        with self.assertRaises(ValueError) as context:
            uncurry_explicit(lambda x: print(x), -1)

        self.assertTrue(NEGATIVE_ARITY_ERROR_MESSAGE in extract_message_string_from_context(context))

    def test_should_raise_error_when_calling_uncurried_function_with_less_arguments_then_passed_arity_is(self):
        with self.assertRaises(ValueError) as context:
            uncurried_function = uncurry_explicit(lambda x: lambda y: x + y, 3)
            result = uncurried_function(1, 2)

        self.assertTrue(BIGGER_ARITY_ERROR_MESSAGE in extract_message_string_from_context(context))

    def test_should_raise_error_when_calling_uncurried_function_with_more_arguments_then_passed_arity_is(self):
        with self.assertRaises(ValueError) as context:
            uncurried_function = uncurry_explicit(lambda x: lambda y: x + y, 1)
            result = uncurried_function(1, 2)

        self.assertTrue(SMALLER_ARITY_ERROR_MESSAGE in extract_message_string_from_context(context))

    def test_should_curry_and_uncurry_example_functions(self):
        f2 = curry_explicit((lambda x, y: x + y), 2)
        g2 = uncurry_explicit(f2, 2)
        self.assertEqual(579, f2(123)(456))
        self.assertEqual(579, g2(123, 456))

    def test_should_uncurry_function_with_2_arguments(self):
        def f(arg1: int, arg2: int):
            return arg1 + arg2

        curried_f = curry_explicit(f, 2)
        uncurried_f = uncurry_explicit(curried_f, 2)
        self.assertEqual(10, uncurried_f(3, 7))

    def test_should_uncurry_function_with_0_arguments(self):
        def f():
            return 1

        curried_f = curry_explicit(f, 0)
        uncurried_f = uncurry_explicit(curried_f, 0)
        self.assertEqual(1, uncurried_f())